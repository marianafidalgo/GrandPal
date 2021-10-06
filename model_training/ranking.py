from transformers import AutoModelForCausalLM, AutoModelWithLMHead, AutoTokenizer, AutoModelForSequenceClassification
import torch, pdb
import numpy as np

modelGPT = AutoModelWithLMHead.from_pretrained('DialoGPT_tests/output-dialogpt-final-s')
tokenizerGPT = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')

modelRPT = AutoModelForSequenceClassification.from_pretrained('microsoft/DialogRPT-human-vs-machine')
tokenizerRPT = AutoTokenizer.from_pretrained('microsoft/DialogRPT-human-vs-machine')

np.random.seed(0)
torch.manual_seed(0)

num_gen = 5

class Generator:
    def __init__(self):
        self.tokenizer = tokenizerGPT
        self.model = modelGPT
        self.ix_EOS = self.tokenizer.eos_token_id
        self.model.eval()
        self.cuda = True
        self.model.cuda()

    def tokenize(self, cxt):
        turns = cxt.split(self.tokenizer.eos_token)
        ids = []
        for turn in turns:
            ids += self.tokenizer.encode(turn.strip()) + [self.ix_EOS]
        ids = torch.tensor([ids]).view(1, -1)
        if self.cuda:
            ids = ids.cuda()
        return ids


class Integrated:

    def __init__(self, generator, ranker):
        self.generator = generator
        self.ranker = ranker

    def predict_(self, cxt, wt_ranker, params):
        with torch.no_grad():

          #prob_hyp2 = self.generator.predict_sampling(cxt, **params)
          #print(prob_hyp2)
          input_ids = self.generator.tokenizer.encode(cxt + self.generator.tokenizer.eos_token, return_tensors='pt')
          input_ids = input_ids.cuda()
          generated_outputs = self.generator.model.generate(
              input_ids,
              max_length=200,
              do_sample=True,
              temperature = 0.7,
              top_k=30,
              top_p=0.8,
              return_dict_in_generate=True,
              output_scores=True,
              num_return_sequences = num_gen,
              pad_token_id=self.generator.tokenizer.eos_token_id
        )
        # only use id's that were generated
        # gen_sequences has shape [1, len]
        gen_sequences = generated_outputs.sequences[:, input_ids.shape[-1]:]

        # let's stack the logits generated at each step to a tensor and transform
        # logits to probs
        probs = torch.stack(generated_outputs.scores, dim=1).softmax(-1)  # -> shape [1, 15, vocab_size]

        # now we need to collect the probability of the generated token
        # we need to add a dummy dim in the end to make gather work
        gen_probs_ = torch.gather(probs, 2, gen_sequences[:, :, None]).squeeze(-1)
        gen_probs1 = gen_probs_.cpu()

        prob_hyp = []
        #number of returned sentences
        for i in range(num_gen):
          gen_probs = gen_probs1[i].detach().numpy()
          #remove extra zeros
          for j in range(len(gen_probs)):
            if gen_probs[j] == 0.0:
              gen_probs = np.delete(gen_probs, np.s_[j: len(gen_probs)])
              break
          # sum of the prob logs, divide by len and do exp
          sum_logP = sum(np.log(gen_probs))
          prob = np.exp(sum_logP / (len(gen_probs) + 1))
          hyp = self.generator.tokenizer.decode(gen_sequences[i][:-1], skip_special_tokens=True)   # strip EOS
          #append with sentence
          prob_hyp.append((prob, hyp))

        probs = np.array([prob for prob, _ in prob_hyp])
        hyps = [hyp for _, hyp in prob_hyp]
        if wt_ranker > 0:
            scores_ranker = predict(self.ranker, cxt, hyps)
            #print(scores_ranker,hyps)
            if isinstance(scores_ranker, dict):
                scores_ranker = scores_ranker['final']
            scores = wt_ranker * scores_ranker + (1 - wt_ranker) * probs
        else:
            scores = probs
        ret = []
        for i in range(len(hyps)):
            ret.append((scores[i], probs[i], scores_ranker[i], hyps[i]))
        ret = sorted(ret, key=lambda x:(x[1]),reverse=True)
        #print(ret)
        return ret

def core(m, ids, l_ids, return_logits=False):
    n = ids.shape[0]
    attention_mask = torch.ones_like(ids) # Returns a tensor filled with the scalar value 1, with the same size as input
    #Adjust mask to the size of each hyp
    for i in range(n):
        attention_mask[i, l_ids[i]:] *= 0

    hidden_states, _ = m.transformer(ids, attention_mask=attention_mask, return_dict=False)
    logits = m.score(hidden_states).squeeze(-1)
    logits = torch.stack([logits[i, l_ids[i] - 1] for i in range(n)])
    if return_logits:
        return logits
    else:
        return torch.sigmoid(logits)

def predict(model, cxt, hyps, max_cxt_turn=None):
    # cxt = str
    # hyps = list of str

    model.eval()
    model = model.cuda()
    cxt_turns = cxt.split('<|endoftext|>')
    if max_cxt_turn is not None:
        cxt_turns = cxt_turns[-min(max_cxt_turn, len(cxt_turns)):]
    ids_cxt = []
    for turn in cxt_turns:
      ids_cxt += tokenizerRPT.encode(turn.strip()) + [50256]
    seqs = []
    lens = []
    for hyp in hyps:
      seq = ids_cxt + tokenizerRPT.encode(hyp.strip())
      lens.append(len(seq))
      seqs.append(seq)
    max_len = max(lens)
    ids = []
    for seq in seqs:
        ids.append(seq + [50256] * (max_len - len(seq)))
    with torch.no_grad():
        ids = torch.LongTensor(ids)
        #if model.opt.cuda:
        ids = ids.cuda()
        scores = core(model, ids, lens)
    if not isinstance(scores, dict):
        #if model.opt.cuda:
        scores = scores.cpu()
        return scores.detach().numpy()

    for k in scores:
        #if model.opt.cuda:
        scores[k] = scores[k].cpu()
        scores[k] = scores[k].detach().numpy()
    return scores

def test(model, path_in, wt_ranker, params, max_n):
    lines = []
    probs = [0,0]
    n_prob = 0
    for i, line in enumerate(open(path_in, encoding='utf-8')):
      #print('processing %i-th context'%i)
      cxt = line.strip('\n').split('\t')[0]
      ret = model.predict_(cxt, wt_ranker, params)
      #cc = [cxt] + [tup[-1] for tup in ret]
      for tup in ret:
        #cc = [cxt] + ['('+ str(tup[-1])+', gen '+str(tup[1])+', rank '+ str(tup[0]) + ')' ]
        cc = [str(tup[-1])]
        probs[0] += tup[1]
        probs[1] += tup[0]
        n_prob += 1
        lines.append('\t'.join(cc))
        #Just to save the one with the highest probability
        break
      if i == max_n:
          break
    probs[:] = [x / n_prob for x in probs]
    #lines.append('\t'.join(["generation probability: " + str(probs[0])+', ranking probability:'+str(probs[1])]))
    print(["generation probability: " + str(probs[0])+', ranking probability:'+str(probs[1])])
    path_out = 'final outquestions.txt' #+ '.hyps'
    with open(path_out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('saved to '+path_out)

generator = Generator()
params = {'temperature': 0.7, 'n_hyp': 5}

#generator.predict = generator.predict_sampling

model_i = Integrated(generator, modelRPT)

test(model_i,"data/questions.txt", 1, params, 3870)