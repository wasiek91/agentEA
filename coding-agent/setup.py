"""Setup script for the AI Coding Agent."""
import os
import sys
from pathlib import Path


def setup():
    """Run setup checks and create necessary files."""
    print("=" * 60)
    print("AI Coding Agent - Setup")
    print("=" * 60)
    print()

    # Check Python version
    print("1. Checking Python version...")
    if sys.version_info < (3, 8):
        print("   [X] Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"   [OK] Python {sys.version_info.major}.{sys.version_info.minor}")
    print()

    # Check if .env exists
    print("2. Checking environment configuration...")
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_file.exists():
        if env_example.exists():
            print("   [!] .env file not found")
            print("   Creating .env from .env.example...")
            env_file.write_text(env_example.read_text())
            print("   [OK] Created .env file")
            print("   [!] Please edit .env and add your ANTHROPIC_API_KEY")
        else:
            print("   [X] .env.example not found")
            return False
    else:
        # Check if API key is set
        env_content = env_file.read_text()
        if "your_api_key_here" in env_content or not any("ANTHROPIC_API_KEY=" in line and len(line.split("=")[1].strip()) > 10 for line in env_content.split("\n")):
            print("   [!] .env exists but ANTHROPIC_API_KEY not configured")
            print("   Please edit .env and add your API key")
        else:
            print("   [OK] .env configured")
    print()

    # Check dependencies
    print("3. Checking dependencies...")
    missing_deps = []

    deps = [
        ("langchain", "langchain"),
        ("langchain_anthropic", "langchain-anthropic"),
        ("langgraph", "langgraph"),
        ("dotenv", "python-dotenv"),
        ("rich", "rich"),
    ]

    for module, package in deps:
        try:
            __import__(module)
            print(f"   [OK] {package}")
        except ImportError:
            print(f"   [X] {package}")
            missing_deps.append(package)

    if missing_deps:
        print()
        print("   Missing dependencies. Install with:")
        print(f"   pip install {' '.join(missing_deps)}")
        print()
        print("   Or install all at once:")
        print("   pip install -r requirements.txt")
        return False

    print()

    # Check optional dependencies
    print("4. Checking optional tools...")

    # Check git
    import subprocess
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("   [OK] git")
        else:
            print("   [!] git (install recommended)")
    except:
        print("   [!] git not found (recommended for version control)")

    # Check aider
    try:
        result = subprocess.run(["aider", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("   [OK] aider")
        else:
            print("   [!] aider (install recommended)")
    except:
        print("   [!] aider not found")
        print("     Install with: pip install aider-chat")

    print()
    print("=" * 60)
    print("Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env and add your ANTHROPIC_API_KEY")
    print("2. (Optional) Install aider: pip install aider-chat")
    print("3. Run the agent:")
    print("   python agent.py --help")
    print("   python agent.py --task 'your task here'")
    print("   python agent.py --interactive")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nSetup error: {e}")
        sys.exit(1)
