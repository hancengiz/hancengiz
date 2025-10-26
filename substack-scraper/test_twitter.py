#!/usr/bin/env python3
"""
Test Twitter posting locally with .env credentials
"""
import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    print(f"✓ Loaded credentials from {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Using environment variables directly...")

import tweepy

def test_twitter_connection():
    """Test Twitter API connection and permissions"""

    # Get credentials from environment
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("✗ Missing credentials. Make sure .env file has all 4 values:")
        print("  - TWITTER_API_KEY")
        print("  - TWITTER_API_SECRET")
        print("  - TWITTER_ACCESS_TOKEN")
        print("  - TWITTER_ACCESS_TOKEN_SECRET")
        return False

    print("\n" + "="*60)
    print("Testing Twitter API Connection")
    print("="*60)

    try:
        # Initialize Twitter client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        print("✓ Twitter client initialized")

        # Get authenticated user info
        me = client.get_me()
        print(f"✓ Authenticated as: @{me.data.username}")
        print(f"  User ID: {me.data.id}")
        print(f"  Name: {me.data.name}")

        print("\n" + "="*60)
        print("✅ SUCCESS! Twitter API is working correctly")
        print("="*60)

        return True

    except tweepy.TweepyException as e:
        print(f"\n✗ Twitter API Error: {e}")

        if "403" in str(e):
            print("\n⚠️  Permission Issue Detected!")
            print("\nTo fix:")
            print("1. Go to: https://developer.twitter.com/en/portal/dashboard")
            print("2. Select your app → Settings")
            print("3. Enable 'Read and write' permissions")
            print("4. Go to 'Keys and tokens' → Regenerate Access Token & Secret")
            print("5. Update .env file with new token values")

        return False

    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        return False

def test_post_tweet(dry_run=True):
    """Test posting a tweet (dry run by default)"""

    if dry_run:
        print("\n" + "="*60)
        print("DRY RUN MODE - Will not actually post")
        print("="*60)
        print("\nTo post a real test tweet, run:")
        print("  python test_twitter.py --post")
        return

    # Get credentials
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        test_tweet = "🧪 Testing automated posting from GitHub Actions\n\n👉 https://github.com/hancengiz/hancengiz"

        print(f"\n📝 Posting test tweet:\n{test_tweet}\n")

        response = client.create_tweet(text=test_tweet)
        tweet_id = response.data['id']

        print(f"✅ Tweet posted successfully!")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/i/web/status/{tweet_id}")

        return True

    except tweepy.TweepyException as e:
        print(f"✗ Failed to post tweet: {e}")
        return False

if __name__ == "__main__":
    import sys

    # Test connection
    success = test_twitter_connection()

    if success:
        # Check if user wants to post a real tweet
        if len(sys.argv) > 1 and sys.argv[1] == '--post':
            print("\n⚠️  WARNING: This will post a real tweet to Twitter!")
            confirm = input("Continue? (yes/no): ")
            if confirm.lower() == 'yes':
                test_post_tweet(dry_run=False)
            else:
                print("Cancelled.")
        else:
            test_post_tweet(dry_run=True)
