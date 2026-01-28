#!/usr/bin/env python3
"""
Claude CLI - Spawn and manage Claude workers in tmux sessions.

Usage:
    uv run python main.py spawn "Your prompt here"
    uv run python main.py spawn --name my-worker "Your prompt"
    uv run python main.py capture my-worker --lines 50
    uv run python main.py list
    uv run python main.py kill my-worker
    uv run python main.py kill-all
"""

import subprocess
import time
import uuid
from pathlib import Path

import click


def run_tmux(*args: str) -> subprocess.CompletedProcess:
    """Execute a tmux command and return the result."""
    return subprocess.run(
        ["tmux", *args],
        capture_output=True,
        text=True,
    )


def generate_session_name() -> str:
    """Generate a unique session name."""
    return f"claude-{uuid.uuid4().hex[:8]}"


def session_exists(name: str) -> bool:
    """Check if a tmux session exists."""
    result = run_tmux("has-session", "-t", name)
    return result.returncode == 0


def get_claude_sessions() -> list[str]:
    """Get all Claude worker sessions."""
    result = run_tmux("list-sessions", "-F", "#{session_name}")
    if result.returncode != 0:
        return []
    return [s for s in result.stdout.strip().split("\n") if s.startswith("claude-")]


def get_role_context(role: str) -> str | None:
    """Get context from context-cli for a given role."""
    context_cli_path = Path(__file__).parent.parent / "context-cli"
    if not context_cli_path.exists():
        return None

    result = subprocess.run(
        ["uv", "run", "python", "main.py", "show", role],
        capture_output=True,
        text=True,
        cwd=context_cli_path,
    )

    if result.returncode == 0:
        return result.stdout.strip()
    return None


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Claude CLI - Spawn and manage Claude workers in tmux sessions."""
    pass


@cli.command()
@click.argument("prompt")
@click.option("--name", "-n", default=None, help="Session name (auto-generated if not provided)")
@click.option("--role", "-r", default=None, help="Role to apply from context-cli")
def spawn(prompt: str, name: str | None, role: str | None):
    """Spawn a Claude worker in a new tmux session.

    PROMPT is the task to give to the worker.

    Examples:
        spawn "Implement a fibonacci function"
        spawn --name fib-worker "Implement fibonacci"
        spawn --role worker "Fix the bug in auth.py"
    """
    session = name or generate_session_name()

    # Check if session already exists
    if session_exists(session):
        click.echo(f"Error: Session '{session}' already exists", err=True)
        click.echo("Use a different name or kill the existing session", err=True)
        raise SystemExit(1)

    # Build the full prompt with role context if provided
    full_prompt = prompt
    if role:
        context = get_role_context(role)
        if context:
            full_prompt = f"{context}\n\n---\n\nTASK:\n{prompt}"
            click.echo(f"Applied role: {role}")
        else:
            click.echo(f"Warning: Could not load role '{role}'", err=True)

    # Create tmux session with claude
    result = run_tmux("new-session", "-d", "-s", session, "claude")
    if result.returncode != 0:
        click.echo(f"Error creating session: {result.stderr}", err=True)
        raise SystemExit(1)

    # Wait for Claude to initialize
    click.echo(f"Starting Claude in session '{session}'...")
    time.sleep(2)

    # Send the prompt
    run_tmux("send-keys", "-t", session, full_prompt, "Enter")

    click.echo(f"Spawned worker: {session}")
    click.echo(f"Attach with: tmux attach -t {session}")
    click.echo(f"Capture with: uv run python main.py capture {session}")


@cli.command()
@click.argument("session")
@click.option("--lines", "-l", default=30, help="Number of lines to capture (default: 30)")
def capture(session: str, lines: int):
    """Capture output from a worker session.

    SESSION is the name of the tmux session to capture from.

    Examples:
        capture my-worker
        capture my-worker --lines 100
    """
    if not session_exists(session):
        click.echo(f"Error: Session '{session}' not found", err=True)
        click.echo("Use 'list' to see active sessions", err=True)
        raise SystemExit(1)

    # Capture the pane content
    result = run_tmux("capture-pane", "-t", session, "-p")
    if result.returncode != 0:
        click.echo(f"Error capturing session: {result.stderr}", err=True)
        raise SystemExit(1)

    # Get the last N lines
    output_lines = result.stdout.strip().split("\n")
    for line in output_lines[-lines:]:
        click.echo(line)


@cli.command("list")
def list_sessions():
    """List all active Claude worker sessions.

    Shows session name and basic info for all sessions
    starting with 'claude-'.
    """
    sessions = get_claude_sessions()

    if not sessions:
        click.echo("No active workers")
        return

    click.echo("Active workers:")
    for session in sessions:
        # Get session info
        result = run_tmux(
            "list-sessions",
            "-F",
            "#{session_name}: created #{session_created_string}",
            "-f",
            f"#{{==:#{session_name},{session}}}",
        )
        if result.returncode == 0 and result.stdout.strip():
            click.echo(f"  - {result.stdout.strip()}")
        else:
            click.echo(f"  - {session}")


@cli.command()
@click.argument("session")
def kill(session: str):
    """Kill a specific worker session.

    SESSION is the name of the tmux session to kill.

    Example:
        kill my-worker
    """
    if not session_exists(session):
        click.echo(f"Error: Session '{session}' not found", err=True)
        raise SystemExit(1)

    result = run_tmux("kill-session", "-t", session)
    if result.returncode != 0:
        click.echo(f"Error killing session: {result.stderr}", err=True)
        raise SystemExit(1)

    click.echo(f"Killed: {session}")


@cli.command("kill-all")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt")
def kill_all(force: bool):
    """Kill all Claude worker sessions.

    Kills all tmux sessions starting with 'claude-'.

    Examples:
        kill-all
        kill-all --force
    """
    sessions = get_claude_sessions()

    if not sessions:
        click.echo("No Claude sessions to kill")
        return

    click.echo(f"Found {len(sessions)} Claude session(s):")
    for session in sessions:
        click.echo(f"  - {session}")

    if not force:
        if not click.confirm("Kill all these sessions?"):
            click.echo("Aborted")
            return

    killed = 0
    for session in sessions:
        result = run_tmux("kill-session", "-t", session)
        if result.returncode == 0:
            killed += 1
        else:
            click.echo(f"Warning: Could not kill {session}", err=True)

    click.echo(f"Killed {killed} session(s)")


@cli.command()
@click.argument("session")
@click.argument("text")
def send(session: str, text: str):
    """Send text to a worker session (advanced).

    Useful for sending commands like /exit to workers.

    Examples:
        send my-worker "/exit"
        send my-worker "continue with the next step"
    """
    if not session_exists(session):
        click.echo(f"Error: Session '{session}' not found", err=True)
        raise SystemExit(1)

    run_tmux("send-keys", "-t", session, text, "Enter")
    click.echo(f"Sent to {session}: {text[:50]}{'...' if len(text) > 50 else ''}")


if __name__ == "__main__":
    cli()
