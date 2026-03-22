from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN
import database
import asyncio

# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Task Manager Bot!\n\n"
        "📌 Commands:\n"
        "/addtask <task>\n"
        "/mytasks\n"
        "/deletetask <task number>\n"
        "/cleartasks\n"
        "/counttasks\n"
        "/remind <seconds> <message>"
    )

# ✅ Add Task
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task_text = " ".join(context.args)

    if not task_text:
        await update.message.reply_text("❌ Please provide a task")
        return

    database.add_task(user_id, task_text)
    await update.message.reply_text("✅ Task added!")

# ✅ View Tasks
async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = database.get_tasks(user_id)

    if not user_tasks:
        await update.message.reply_text("📭 No tasks found")
        return

    message = "📋 Your Tasks:\n\n"
    for i, (task_id, task, created_at) in enumerate(user_tasks, 1):
        message += f"{i}. {task} (🕒 {created_at})\n"

    await update.message.reply_text(message)

# ✅ Delete Task
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

# ✅ Clear All Tasks
async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    database.clear_tasks(user_id)
    await update.message.reply_text("🧹 All tasks cleared!")

# ✅ Count Tasks
async def count_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = database.count_tasks(user_id)
    await update.message.reply_text(f"📊 You have {count} tasks")

# ✅ Reminder Feature
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = int(context.args[0])
        message = " ".join(context.args[1:])

        await update.message.reply_text(f"⏳ Reminder set for {seconds} seconds")

        await asyncio.sleep(seconds)

        await update.message.reply_text(f"⏰ Reminder: {message}")

    except:
        await update.message.reply_text("❌ Usage: /remind <seconds> <message>")

# 🚀 Main Function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("mytasks", my_tasks))
    app.add_handler(CommandHandler("deletetask", delete_task))
    app.add_handler(CommandHandler("cleartasks", clear_tasks))
    app.add_handler(CommandHandler("counttasks", count_tasks))
    app.add_handler(CommandHandler("remind", remind))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
