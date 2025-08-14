# main.py
import asyncio
import os
import sys
from dotenv import load_dotenv
from content_extractor import ContentExtractor
from ai_analyzer import GeminiSkepticAnalyzer
from report_generator import MarkdownReportGenerator

# Load environment variables
load_dotenv()

def print_banner():
    """Print application banner"""
    print("""
🔍 DIGITAL SKEPTIC AI
====================
Powered by Gemini-2.5-pro
Critical Analysis of News Articles
====================
    """)

def validate_api_key():
    """Validate that API key is available"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with your Gemini API key:")
        print("GEMINI_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key

def get_user_input():
    """Get URL input from user"""
    print("📰 Enter the news article URL you want to analyze:")
    url = input("URL: ").strip()
    
    if not url:
        print("❌ Error: No URL provided")
        sys.exit(1)
    
    return url

async def main():
    """Main application logic"""
    try:
        # Print banner
        print_banner()
        
        # Validate API key
        validate_api_key()
        
        # Get user input
        url = get_user_input()
        
        print(f"\n🔄 Starting analysis of: {url}")
        print("=" * 60)
        
        # Initialize components
        print("🛠️ Initializing components...")
        extractor = ContentExtractor()
        analyzer = GeminiSkepticAnalyzer()
        reporter = MarkdownReportGenerator()
        
        # Extract content
        print("\n📥 Step 1: Extracting article content...")
        try:
            article_data = await extractor.extract_content(url)
            print(f"✅ Content extracted: {article_data['extracted_length']} characters")
        except Exception as e:
            print(f"❌ Content extraction failed: {str(e)}")
            print("\n💡 Troubleshooting tips:")
            print("- Check if the URL is accessible")
            print("- Some sites may block automated requests")
            print("- Try a different news article URL")
            return
        
        # Analyze content
        print("\n🧠 Step 2: AI Analysis (this may take a few minutes)...")
        try:
            analysis = await analyzer.analyze_article(
                article_data['content'], 
                article_data['metadata']
            )
            print("✅ AI analysis completed successfully")
        except Exception as e:
            print(f"❌ AI analysis failed: {str(e)}")
            print("\n💡 Possible issues:")
            print("- API rate limits exceeded")
            print("- Network connectivity problems")
            print("- Article content too long or complex")
            return
        
        # Generate report
        print("\n📝 Step 3: Generating analysis report...")
        try:
            report = reporter.generate_report(article_data, analysis)
            print("✅ Report generated successfully")
        except Exception as e:
            print(f"❌ Report generation failed: {str(e)}")
            return
        
        # Save report
        print("\n💾 Step 4: Saving report...")
        try:
            # Create outputs directory if it doesn't exist
            os.makedirs('outputs', exist_ok=True)
            
            # Generate filename
            title = article_data.get('metadata', {}).get('title', 'untitled')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limit length
            
            filename = f"outputs/skeptic_analysis_{safe_title}_{hash(url) % 10000}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ Report saved as: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}")
            print("Report content will be displayed below instead.")
        
        # Display results
        print("\n" + "=" * 60)
        print("📄 ANALYSIS REPORT")
        print("=" * 60)
        print(report)
        
        print("\n🎉 Analysis complete!")
        print("💡 Review the report above for detailed insights about this article.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
