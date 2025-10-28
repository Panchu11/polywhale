"""
Setup script for PolyWhale bot
"""
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(e.stderr)
        return False


def main():
    """Main setup function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🐋 PolyWhale Bot Setup 🐋                   ║
    ║                                                           ║
    ║        Track the smartest money in prediction markets    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("✗ Python 3.11 or higher is required")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("\n⚠ .env file not found")
        print("  Creating .env from .env.example...")
        
        env_example = Path(".env.example")
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✓ .env file created")
            print("\n⚠ IMPORTANT: Edit .env file with your credentials:")
            print("  1. TELEGRAM_BOT_TOKEN (from @BotFather)")
            print("  2. DATABASE_URL (from Supabase)")
            print("  3. REDIS_URL (from Upstash) - optional")
        else:
            print("✗ .env.example not found")
            sys.exit(1)
    else:
        print("✓ .env file exists")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    ):
        sys.exit(1)
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    Setup Complete! 🎉                     ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Next steps:
    
    1. Edit .env file with your credentials:
       - Get Telegram bot token from @BotFather
       - Get database URL from Supabase
       - (Optional) Get Redis URL from Upstash
    
    2. Initialize database:
       python scripts/init_db.py
    
    3. Test the setup:
       python scripts/test_bot.py
       python scripts/test_db.py
       python scripts/test_api.py
    
    4. Run the bot:
       python main.py
    
    For detailed instructions, see GETTING_STARTED.md
    
    Happy whale tracking! 🐋
    """)


if __name__ == "__main__":
    main()

