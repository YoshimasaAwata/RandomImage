import launch

if not launch.is_installed("abc"):
    launch.run_pip("install abc", "abc for RandomImage extension")
