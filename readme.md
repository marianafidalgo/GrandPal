<!--
*** Thanks


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<!-- <br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
</p> -->



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Master Thesis: Open-domain Conversational Agent based on Pre-Trained Transformers for Elderly-Robot Interaction (ongoing)

Motivation:
* A project that solves a problem and helps others
* Increase knowledge in Deep Learning
* Master Thesis

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [DialoGPT](https://huggingface.co/microsoft/DialoGPT-small)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)


<!-- GETTING STARTED -->
## Getting Started

TODO

### Prerequisites

* List of things you need:
  ```sh
  pip install -r requirements.txt
  ```

### Mini-Babel

When it comes to evaluating the performance, the ideal would be to have a human-based evaluation.
Specially in a system where paraphrasing can lead to inferior metrics, despite still having a good performance.
Consequently, to add a score to the translated dataset, a small interface was developed.
In this User Interface: http://20.108.185.129:8501/ , from a dataset storing almost 8000 source and target segments pairs, 14 random are displayed to the user. The user has then the option to classify the translation from 1-10.

## GrandPal-Chat

To add a score to the performance of the Chatbot, a small interface was developed. In this User Interface: http://20.108.185.129:8052/ ,
the user has a chance to engage in a conversation with the system.
After a six utterance interaction with the system, the user has then the option to classify the conversation from 1-10.
One more advantage of this evaluation is allowing to analyze the ability of the model to have context during the dialogue.
Since the system, when predicting a new reply, has the conversation history as input.
Considering that the model was only trained with 7 sentences for context, the input only stores the last 6 uttered sentences.

## GrandPal-Model

* model-app: has the code to build the bot along with a zip contained the fine-tuned model
* model-training: has the code to train and evaluate the model, along with the directory containing the datasets
* mt-api: has the zip containing the mt open source model
* raspberry: has the code to give the bot a body (specifically a Raspberry Pi Zero W). Running the client in the raspberry and the server on a computer, it is possible to build a physical voice assistant. It also comprises a weather and radio API.


<!-- CONTACT -->
## Contact

Mariana Fidalgo

Project Link: [https://github.com/marianafidalgo/GrandPal](https://github.com/marianafidalgo/GrandPal)







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png -->