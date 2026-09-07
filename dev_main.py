try:
    from src.main import main
except ImportError:
    print(
        "Failed to import main from src.main. Ensure that the src directory is in your PYTHONPATH or source scripts/env_bash."
    )

if __name__ == "__main__":
    main()
