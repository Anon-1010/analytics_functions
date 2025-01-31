import asyncio
import threading
from flask import Flask, render_template
import logging
from analytics_functions import (
    load_dummy_data,
    group_sentiment_pulse,
    message_impact_score,
    message_trend_tracker,
    user_activity_clusters,
    group_cohesion_index,
    bot_vs_human_engagement_ratio,
    group_content_engagement_diversity,
    group_activity_heatmap,
    top_contributor_influence,
    message_lifespan
)
from telegram import Bot
from telegram.ext import CommandHandler, Application
import signal
import sys

# Set up Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO)
error_log = logging.getLogger('error_logger')
error_log.addHandler(logging.FileHandler('logs/error.log'))

TOKEN = "8157213:AAGLMk2iZt6JStxMxojw"
bot = Bot(token=TOKEN)


def start(update, context):
    """Start command that sends a greeting message."""
    update.message.reply_text("Hello! I am your bot. Use /analytics to get group analytics.")

# Function to fetch analytics data
def analytics(update, context):
    """Fetch and send the analytics data to the user."""
    groups_df, members_df, messages_df = load_dummy_data()

    analytics_results = {
        "Group Sentiment": group_sentiment_pulse(messages_df),
        "Message Impact": message_impact_score(messages_df),
        "Message Trend": message_trend_tracker(messages_df),
        "User Activity": user_activity_clusters(members_df),
        "Group Cohesion": group_cohesion_index(messages_df),
        "Bot vs Human Engagement": bot_vs_human_engagement_ratio(members_df),
        "Content Diversity": group_content_engagement_diversity(messages_df),
        "Activity Heatmap": group_activity_heatmap(messages_df),
        "Top Contributors": top_contributor_influence(messages_df),
        "Message Lifespan": message_lifespan(messages_df)
    }

    # Send analytics results to user
    message = "Here are the analytics results:\n"
    for key, value in analytics_results.items():
        message += f"{key}: {value}\n"

    update.message.reply_text(message)

# Set up the updater and dispatcher for the bot
application = Application.builder().token(TOKEN).build()

# Add the handlers for the bot commands
start_handler = CommandHandler('start', start)
analytics_handler = CommandHandler('analytics', analytics)

application.add_handler(start_handler)
application.add_handler(analytics_handler)


@app.route('/')
def dashboard():
    print("Dashboard route hit!")
    groups_df, members_df, messages_df = load_dummy_data()

    # Call analytics functions for the dashboard
    analytics_results = {
        "group_sentiment": group_sentiment_pulse(messages_df),
        "message_impact": message_impact_score(messages_df),
        "message_trend": message_trend_tracker(messages_df),
        "user_activity": user_activity_clusters(members_df),
        "group_cohesion": group_cohesion_index(messages_df),
        "bot_human_ratio": bot_vs_human_engagement_ratio(members_df),
        "content_diversity": group_content_engagement_diversity(messages_df),
        "activity_heatmap": group_activity_heatmap(messages_df),
        "top_contributors": top_contributor_influence(messages_df),
        "message_lifespan": message_lifespan(messages_df)
    }

    print(analytics_results)

    return render_template('dashboard.html', data=analytics_results)

# Function to start the bot polling using asyncio
async def start_telegram_bot():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.stop()


def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(application.shutdown())
    sys.exit(0)


def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  

    
    try:
        loop.run_until_complete(start_telegram_bot())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
    finally:
        loop.close()

if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()

    
    app.run(debug=True)
