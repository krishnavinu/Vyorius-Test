# AI Comment Moderation System

A Python application that detects offensive content in user comments using both local profanity filtering and Groq's LLaMA AI model, with detailed reporting and visualization capabilities.

## Features

- 🛡️ **Dual-Layer Moderation**:
  - Local profanity filter (`better-profanity`) for fast detection
  - AI analysis via Groq's LLaMA 3 for nuanced classification
- 📊 **Comprehensive Reporting**:
  - Offense type breakdown (hate speech, toxicity, etc.)
  - Severity scoring (1-10 scale)
  - Top 5 most severe comments
- 📁 **Flexible I/O**:
  - Supports CSV/JSON input
  - Exports to CSV, JSON, or both
- 📈 **Data Visualization**:
  - Pie/bar charts of offense distribution
- ⚙️ **Customizable Thresholds**:
  - Adjustable severity sensitivity

## Requirements

- Python 3.8+
- [Groq API key](https://console.groq.com/)

## Install dependecy

1. pip install -r requirements.txt

## Setup api key
- create .env file
- add this in the file:
- GROQ_API_KEY=your_api_key_here

## Sample input

add the sample input
