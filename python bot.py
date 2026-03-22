from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN
import database

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Commands:\n"
        "/addtask <task>\n"
        "/mytasks\n"
        "/deletetask <task number>"
    )

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = " ".join(context.args)

    if not task_text:
        await update.message.reply_text("❌ Please provide a task")
        return

    database.add_task(user_id, task_text)
    await update.message.reply_text("✅ Task added!")

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = database.get_tasks(user_id)

    if not user_tasks:
        await update.message.reply_text("No tasks found")
        return

    message = "📋 Your Tasks:\n"
    for i, (task_id, task) in enumerate(user_tasks, 1):
        message += f"{i}. {task}\n"

    await update.message.reply_text(message)

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = database.get_tasks(user_id)

    try:
        index = int(context.args[0]) - 1
        task_id = user_tasks[index][0]
        database.delete_task(task_id)
        await update.message.reply_text("🗑 Task deleted")
    except:
        await update.message.reply_text("❌ Invalid task number")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("mytasks", my_tasks))
    app.add_handler(CommandHandler("deletetask", delete_task))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
