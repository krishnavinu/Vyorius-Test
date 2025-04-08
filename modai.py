import pandas as pd
import argparse
import requests
import os
import json
from tqdm import tqdm
from better_profanity import profanity
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import time
import sys

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure profanity filter
profanity.load_censor_words()

# API configuration
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def validate_input_file(file_path):
    """Validate the input file exists and has correct format"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or JSON")
    
    required_cols = ["comment_id", "username", "comment_text"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    if df.empty:
        raise ValueError("Input file is empty")
    
    return df

def call_llama_moderation(comment):
    """Analyze comment for offensive content using LLAMA API"""
    prompt = f"""Analyze this comment for offensive content. Return JSON with:
- is_offensive (boolean)
- offense_type (string: hate_speech, toxicity, profanity, harassment, or none)
- severity (1-10)
- explanation (string)

Comment: "{comment}"

Return ONLY valid JSON with no additional text or formatting."""
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=HEADERS, json=data, timeout=15)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        
        try:
            result = json.loads(content)
            required_fields = ["is_offensive", "offense_type", "severity", "explanation"]
            if not all(field in result for field in required_fields):
                raise ValueError("Missing required fields in API response")
            return result
        except json.JSONDecodeError:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(content[start:end])
            raise ValueError("Could not extract valid JSON from response")
            
    except requests.exceptions.RequestException as e:
        print(f"\nAPI Request failed: {str(e)}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"\nError processing API response: {str(e)}", file=sys.stderr)
        return None

def process_comments(df, min_severity=1):
    """Process comments through profanity filter and AI moderation"""
    results = []
    print("\nProcessing comments through moderation system...")
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Analyzing comments"):
        comment = row['comment_text']
        result = {
            "comment_id": row['comment_id'],
            "username": row['username'],
            "comment_text": comment,
            "is_offensive": False,
            "offense_type": None,
            "severity": 0,
            "explanation": "Pending analysis"
        }

        if profanity.contains_profanity(comment):
            result.update({
                "is_offensive": True,
                "offense_type": "profanity",
                "severity": 5,
                "explanation": "Detected by local profanity filter"
            })
        else:
            llama_result = call_llama_moderation(comment)
            if llama_result:
                result.update(llama_result)
            else:
                result["explanation"] = "Analysis failed"
            time.sleep(0.5)

        # Apply severity threshold
        if result["severity"] < min_severity:
            result["is_offensive"] = False
            
        results.append(result)
    
    return pd.DataFrame(results)

def generate_report(analyzed_df):
    """Generate detailed moderation report"""
    offensive = analyzed_df[analyzed_df["is_offensive"] == True]
    
    print("\n=== MODERATION REPORT ===")
    print(f"\n📊 Basic Statistics:")
    print(f"• Total comments processed: {len(analyzed_df)}")
    print(f"• Offensive comments found: {len(offensive)} ({len(offensive)/len(analyzed_df):.1%})")
    
    if not offensive.empty:
        print("\n🔍 Offense Type Analysis:")
        offense_counts = offensive["offense_type"].value_counts()
        for offense, count in offense_counts.items():
            print(f"• {offense.title()}: {count} cases")
        
        print("\n⚠️ Severity Distribution:")
        severity_stats = offensive["severity"].describe()
        print(f"• Average severity: {severity_stats['mean']:.1f}/10")
        print(f"• Maximum severity: {severity_stats['max']}/10")
        print(f"• Minimum severity: {severity_stats['min']}/10")
        
        print("\n🚨 Top 5 Most Severe Comments:")
        top_offenders = offensive.sort_values("severity", ascending=False).head(5)
        for idx, (_, row) in enumerate(top_offenders.iterrows(), 1):
            print(f"\n#{idx} 🔥 Severity: {row['severity']}/10")
            print(f"👤 User: {row['username']}")
            print(f"📝 Comment: {row['comment_text']}")
            print(f"🔖 Type: {row['offense_type'].title()}")
            print(f"💬 Analysis: {row['explanation']}")
    else:
        print("\n✅ No offensive comments detected")

def generate_visualizations(analyzed_df, chart_type="pie"):
    """Generate visualizations based on chart type"""
    offensive = analyzed_df[analyzed_df["is_offensive"] == True]
    
    if offensive.empty:
        print("\nNo offensive comments to visualize.")
        return
    
    offense_counts = offensive["offense_type"].value_counts()
    
    if chart_type in ["pie", "both"]:
        plt.figure(figsize=(8, 8))
        offense_counts.plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05]*len(offense_counts),
            colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'],
            wedgeprops={'edgecolor': 'black', 'linewidth': 1}
        )
        plt.title("Distribution of Offense Types", pad=20)
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig("offense_types_pie.png", dpi=300)
        print("\n📈 Saved pie chart as 'offense_types_pie.png'")
        plt.close()
    
    if chart_type in ["bar", "both"]:
        plt.figure(figsize=(10, 6))
        offense_counts.plot.bar(color='#ff6b6b', edgecolor='black')
        plt.title("Offense Type Distribution")
        plt.ylabel("Number of Comments")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("offense_types_bar.png", dpi=300)
        print("📊 Saved bar chart as 'offense_types_bar.png'")
        plt.close()

def parse_arguments():
    """Configure and parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AI Comment Moderation System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "input_file",
        help="Path to input file (CSV or JSON)"
    )
    parser.add_argument(
        "--output-format",
        choices=["csv", "json", "both"],
        default="both",
        help="Output file format(s)"
    )
    parser.add_argument(
        "--chart-type",
        choices=["bar", "pie", "both", "none"],
        default="pie",
        help="Type of chart to generate"
    )
    parser.add_argument(
        "--min-severity",
        type=int,
        default=1,
        help="Minimum severity score to consider offensive (1-10)",
        metavar="SEVERITY"
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()

    try:
        df = validate_input_file(args.input_file)
        print(f"\nLoaded {len(df)} comments from {args.input_file}")
        print("\nSample comments:")
        print(df[["comment_id", "username", "comment_text"]].head(5).to_string(index=False))
        
        analyzed_df = process_comments(df, args.min_severity)
        
        base_name = os.path.splitext(args.input_file)[0]
        
        if args.output_format in ["csv", "both"]:
            csv_file = f"{base_name}_analyzed.csv"
            analyzed_df.to_csv(csv_file, index=False)
            print(f"\n💾 Saved CSV results to '{csv_file}'")
        
        if args.output_format in ["json", "both"]:
            json_file = f"{base_name}_analyzed.json"
            analyzed_df.to_json(json_file, orient="records", indent=2)
            print(f"💾 Saved JSON results to '{json_file}'")

        generate_report(analyzed_df)
        
        if args.chart_type != "none":
            generate_visualizations(analyzed_df, args.chart_type)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()