# PearceGolf
A lan accessed multiplayer game written in python using arcade.

# Overview

I wanted to create a multidevice card golf game that could be played across lan. I wanted it to be able to track player movements and pass that information to the other player. This project is unfinished. I intend on coming back to it to deepen my understanding of the code. I made TwistGolf and was really happy with how it turned out. When I went to make it into a networked game, I realized I couldn't use it because it was written with Tkinter which doesn't support multiplayer lan. I rewrote my program in Arcade and felt like it was so much more sophisticated! Sadly, I struggled with connecting it to a server.

[Software Demo Video](https://youtu.be/UOlUqVCgSSs)

# Network Communication

I was using a client/server model. I opted to use pickle for serializing data. Socket was to be used for the network conections.

TCP? I honestly got so confused with this one. I didn't feel like I found a lot of tutorials that explained this very well. The main papers felt like a wall of text and i struggled a lot with understanding the concepts.

Format is serialized data.

# Development Environment

Socket and pickle were the tools I was using for this. I coded it in VS code.

Python with arcade was used as the language.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Tech with Tim](https://www.youtube.com/@TechWithTim)
* [Python Arcade Library](https://api.arcade.academy/en/latest/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* make it work.
* Add points
* End turn properly