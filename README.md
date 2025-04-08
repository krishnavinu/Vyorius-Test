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

##  Installation

### Clone the Repository
- ```bash
    https://github.com/krishnavinu/Vyorius-Test.git

## Install dependecy
- ```bash
  pip install -r requirements.txt

## Setup api key
- create .env file
- add this in the file:
  ```bash
  GROQ_API_KEY=your_api_key_here

## Sample input
CSV Format (comments.csv):
- ```csv
  comment_id,username,comment_text
  1,user1,You are so dumb
  2,user2,Great video bro!
  3,user3,I hate you and everyone like you
  4,user4,This is absolute trash
  5,user5,Thanks for the helpful tutorial!
  6,user6,You're a worthless piece of garbage
JSON Format (comments.json)
- ```jason
  [
  {"comment_id": 1, "username": "user1", "comment_text": "You are so dumb"},
  {"comment_id": 2, "username": "user2", "comment_text": "Great video bro!"},
  {"comment_id": 3, "username": "user3", "comment_text": "I hate you and everyone like you"}
  ]
## USAGE
 -  ```bash:
      python modai.py input.json --output-format both --chart-type both  --min-severity 5

- --output-format both [can change between csv or jason]
- --chart-type both [can change between pie or bar]
- --min-severity 5 [adjust from 1-10]
## Samle Output:
- ```bash
       python modai.py input.json --output-format both --chart-type both --min-severity 5
- ```bash 
    Loaded 21 comments from input.json

  Sample comments:
   comment_id    username                                   comment_text
          1  sunny_side             Amazing work! Really enjoyed this.
          2   rageboy77 This is total trash, go learn something first.
          3  happyvibes            Sending you love and good energy! 😊
          4 darkwarrior      This is the dumbest thing I've ever seen.
          5   kindheart      Thank you for sharing this, very helpful!

  Processing comments through moderation system...
  Analyzing comments: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 21/21       [00:20<00:00,  1.00it/s] 

  💾 Saved CSV results to 'input_analyzed.csv'
  💾 Saved JSON results to 'input_analyzed.json'

  === MODERATION REPORT ===

  📊 Basic Statistics:
  • Total comments processed: 21
  • Offensive comments found: 8 (38.1%)

  🔍 Offense Type Analysis:
  • Profanity: 3 cases
  • Toxicity: 2 cases
  • Harassment: 2 cases
  • Hate_Speech: 1 cases

  ⚠️ Severity Distribution:
  • Average severity: 7.1/10
  • Maximum severity: 10.0/10
  • Minimum severity: 5.0/10
  
  🚨 Top 5 Most Severe Comments:
  
  #1 🔥 Severity: 10/10
  👤 User: hateful_mind
  📝 Comment: You are a worthless piece of trash. People like you should be eliminated from society. I hope you suffer.
  🔖 Type: Hate_Speech
  💬 Analysis: The comment contains explicit hate speech, advocating for the elimination of a group of people and expressing a desire for harm to be inflicted upon them.        
  
  #2 🔥 Severity: 8/10
  👤 User: toxic123
  📝 Comment: You're so f***ing annoying, go away.
  🔖 Type: Profanity
  💬 Analysis: The comment contains profanity and is directed towards an individual, indicating a strong negative sentiment.
  
  #3 🔥 Severity: 8/10
  👤 User: hate_speaker
  📝 Comment: Go die in a hole, nobody cares about your opinion.
  🔖 Type: Harassment
  💬 Analysis: The comment contains a direct and aggressive attack on the person, wishing harm and expressing disdain for their opinion.
  
  #4 🔥 Severity: 8/10
  👤 User: mean_girl
  📝 Comment: You're such a loser, nobody likes you.
  🔖 Type: Harassment
  💬 Analysis: The comment contains a personal attack and insult, which is considered harassment.
  
  #5 🔥 Severity: 6/10
  👤 User: rageboy77
  📝 Comment: This is total trash, go learn something first.
  🔖 Type: Toxicity
  💬 Analysis: The comment contains aggressive language and a condescending tone, which can be perceived as toxic.
  
  📈 Saved pie chart as 'offense_types_pie.png'
  📊 Saved bar chart as 'offense_types_bar.png'
  
## Output file
- input_analyzed.csv
- input_analyzed.jason
  
## Sample Graph
![offense_types_pie](https://github.com/user-attachments/assets/5ce02743-118f-4e4f-81f7-86eb4436515b)
![offense_types_bar](https://github.com/user-attachments/assets/116e0cda-cdbd-4279-928e-632899152924)

