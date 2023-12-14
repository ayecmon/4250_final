# Search Engine

Using python, this project demostrates how search engine works.

## Table of Contents

- [Introduction](#introduction)
- [Branches](#Branches)
- [Features](#Features)
- [Contributors](#contributors)

## Introduction
The goal of this project is to gather information about professors in the Biology department by crawling their profiles on a website. The project utilizes Python libraries for web crawling, HTML parsing, text processing, and data storage in MongoDB.

## Branches

This project follows a branching strategy to organize different tasks and features. The main branches include:

- **main:** The main branch is the production-ready code which includes biology.py and searchengine.py.
- **index_counts:** This branch includes implementation of indexing and search engine.

## Features
- Demo Video
https://livecsupomona-my.sharepoint.com/:v:/g/personal/acmon_cpp_edu/EaOtasUUb-1FuZDbI9FkMkYByF0CWU448okABj8mJsBB-g?e=7idlMV&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D

## Contributors

- [Aye Mon (@ayecmon)](https://github.com/ayecmon)
  - implements crawlerThread function and skeleton of crawler.

- [Alejandro Mora-Lopez (@amora7741)](https://github.com/amora7741)
  - implements the ‘parse’ function in the crawler. This function allowed every relevant link to be stored in order for the crawler to visit.
  - 
- [Francisco Serrano (@franserr99)](https://github.com/franserr99)
  - implements target function. This function identified relevant pages, which were found by following a default page pattern

- [Kevin Vi (@kvicode)](https://github.com/kvicode)
  - was in charge to parse faculty data and indexing it

- [Davit Barseghyan (@davitbars)](https://github.com/davitbars)
  - implements searchengine.py
