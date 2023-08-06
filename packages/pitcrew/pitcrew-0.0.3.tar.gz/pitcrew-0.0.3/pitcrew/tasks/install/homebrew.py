from pitcrew import task


class InstallHomebrew(task.BaseTask):
    """Installs the homebrew package manager"""

    async def verify(self):
        await self.install.xcode_cli()
        assert await self.sh("which brew")

    async def run(self):
        await self.sh(
            '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'
        )
