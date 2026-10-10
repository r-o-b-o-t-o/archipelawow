# 🌍 ArchipelaWoW

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![APWorld](https://github.com/r-o-b-o-t-o/archipelawow/actions/workflows/apworld.yml/badge.svg)](https://github.com/r-o-b-o-t-o/archipelawow/actions/workflows/apworld.yml)

> [!WARNING]
> ArchipelaWoW is still very much in its infancy. Expect generation errors, features can be partly implemented, and more features are planned but not added yet.

An [APWorld](https://archipelago.miraheze.org/wiki/APWorld) definition for the [AzerothCore](https://www.azerothcore.org/) World of Warcraft server emulator, providing specific progression logic for [Archipelago](https://github.com/ArchipelagoMW/Archipelago) - a multi-game multi-world randomizer framework.

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Installation & Usage](#-installation--usage)
- [Development](#%EF%B8%8F-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🏰 About

ArchipelaWoW brings the magic of World of Warcraft to the Archipelago randomizer ecosystem. Experience Azeroth like never before with randomized progression and items across multiple worlds!

## ✨ Features

### 🎯 Location Checks
These are the actions you take in-game to send rewards to yourself or other players in the multiworld, creating interconnected progression across different games and worlds.

- **Dungeon Completions & Bosses**
- **Achievements**
- **Flight Paths**
- **Quests**
- **Exploration**: Discovering the subzones the exploration achievements ask for
- **Experience Gains**: Gaining experience completes checks but doesn't level up your character normally - your actual level stays the same until you receive level-up rewards
- **Spell Training**: Buying the first rank of a class spell, a weapon skill or a riding rank from your trainer sends a check instead of teaching it
- **Weapon Skills & Defense**: Raising skills to several level caps sends checks

### 🎁 Randomized Rewards
- **Items**: Receive powerful gear and artifacts at unexpected times
- **Zone Unlocks**: Access new areas through randomized progression
- **Level Ups**: Increase your character level - these can be sent by other players or by completing location checks
- **Spells & Skills**: The first rank of each class spell, plus the weapon skills your class can learn, arrive from the multiworld - once you have a first rank, your trainer sells the higher ones as usual
- **Progressive Riding Skill**
- **Progressive Upgrades**: Movement speed and experience rate bonuses to help you progress faster
- **Eternal Food & Drink**: No more visiting the innkeeper every 2 hours
- **Scroll of Divination**: Hints 3 of your world's unchecked locations
- **Tome of Insight**: Grants a quarter of the experience needed for your next level check
- **Teleport to Friend**: Lets the Archipelago Stone teleport you to another World of Warcraft player of the multiworld, every 30 minutes. Only in seeds with more than one World of Warcraft player

## 🚀 Installation & Usage

### ⚡ Easy Installation (Windows)

The [**ArchipelaWoW Launcher**](https://github.com/r-o-b-o-t-o/archipelawow-launcher) installs a ready-to-run AzerothCore server with the ArchipelaWoW module, installs the APWorld in Archipelago, edits player options and tracks your checks on the world maps. Its server comes prebuilt, so it can't take other modules: follow the [manual setup](#-manual-setup) for that.

1. **Install the Launcher**
   - Download it from the [latest release](https://github.com/r-o-b-o-t-o/archipelawow-launcher/releases/latest): `ArchipelaWoW.Launcher-win-Setup.exe` installs it, `ArchipelaWoW.Launcher-win-Portable.zip` keeps everything in the folder you extract it to (keep that folder close to the root of a drive, e.g. `C:\Games\ArchipelaWoW`)

2. **Set Up the Server**
   - Follow the launcher's **Setup** page: it installs the server, the database, the configuration and the client data, then asks who can join the realm (this computer, your local network, or friends over the internet)

3. **Install Archipelago and the APWorld**
   - Download and install [**Archipelago**](https://github.com/ArchipelagoMW/Archipelago/releases)
   - Install the APWorld from the launcher's **APWorld** page

4. **Configure Your Game**
   - Make each player's options on the launcher's **Player options** page
   - Export them to the `Players` folder of your Archipelago installation

5. **Generate and Host Your Multiworld**
   - Click "Generate" in the Archipelago Launcher
   - Upload the game from Archipelago's `output` folder to [archipelago.gg](https://archipelago.gg/uploads), or host it locally by clicking "Host" in the Archipelago Launcher

6. **Connect the Server**
   - Start the servers from the launcher's **Dashboard**
   - Enter your room's server, port and password in its **Archipelago room** card
   - Create a game account in its **Game account** card

7. **Link Your Character**
   - Set `set realmlist 127.0.0.1` in your client's `Data\<locale>\realmlist.wtf`
   - Other players use the address the setup shows instead of `127.0.0.1`
   - Create a fresh character and log in
   - Use command: `.ap connect SlotName` (where SlotName matches your player options)
   - An Archipelago Stone will appear in your inventory for mod interaction

The launcher's [README](https://github.com/r-o-b-o-t-o/archipelawow-launcher#readme) covers updating, playing with friends and the tracker.

### 🔧 Manual Setup

On other systems, or to build AzerothCore with your own modules, set everything up yourself.

#### Prerequisites
- [AzerothCore Server](https://www.azerothcore.org/wiki/classic-installation)
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

#### Step-by-Step Setup

1. **Install AzerothCore**
   - Follow the [**official installation guide**](https://www.azerothcore.org/wiki/classic-installation)

2. **Add the ArchipelaWoW Module**
   - Add [**`mod-I-found-your-sword`**](https://github.com/r-o-b-o-t-o/mod-i-found-your-sword) to your AzerothCore installation

3. **Install Archipelago**
   - Download and install [**Archipelago**](https://github.com/ArchipelagoMW/Archipelago/releases)

4. **Install the APWorld**
   - Download `worldofwarcraft.apworld` from the [Releases page](https://github.com/r-o-b-o-t-o/archipelawow/releases)
   - Install by double-clicking the `.apworld` file, or:
     - Open Archipelago Launcher → "Install APWorld"
     - Or manually place in the `custom_worlds` folder

5. **Configure Your Game**
   - Create `.yaml` files for each player using the "Options Creator" in Archipelago Launcher
   - Place files in the `Players` folder of your Archipelago installation

6. **Generate Your Multiworld**
   - Click "Generate" in the Archipelago Launcher
   - Find your generated game in the `output` folder of your Archipelago installation

7. **Host Your Game**
   - Upload to [archipelago.gg](https://archipelago.gg/uploads) for public hosting
   - Or host locally by clicking "Host" in the Archipelago Launcher

8. **Connect AzerothCore**
   - Edit `archipelawow.conf` in `configs/modules` or `etc/modules`
   - Set `ArchipelaWoW.ArchipelagoServerHost` (e.g., `archipelago.gg` or your public IP address)
   - Set `ArchipelaWoW.ArchipelagoServerPort` (port number from your room)
   - Make sure that `ArchipelaWoW.Enable = 1`

9. **Start Your Server**
   - Start your AzerothCore server (`authserver` and `worldserver`)
   - Or run `reload config` in the `worldserver` console if already running

10. **Link Your Character**
    - Create a fresh character and log in
    - Use command: `.ap connect SlotName` (where SlotName matches your `.yaml` file)
    - An Archipelago Stone will appear in your inventory for mod interaction

## 🛠️ Development

### Prerequisites
- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - the commands below use it, but a plain `venv` + `pip` works just as well

### Setup

1. **Clone Archipelago and this repository**

   ```bash
   git clone https://github.com/ArchipelagoMW/Archipelago.git archipelago
   git clone https://github.com/r-o-b-o-t-o/archipelawow.git archipelago/worlds/worldofwarcraft
   cd archipelago
   ```

2. **Install the dependencies**

   ```bash
   uv python install 3.13
   uv venv --python 3.13
   uv pip install pip
   uv pip install -r requirements.txt
   ```

3. **Write a web host config**

   PowerShell:
   ```powershell
   "PORT: 8080" | Out-File -FilePath "config.yaml"
   ```

   Bash:
   ```bash
   echo "PORT: 8080" > config.yaml
   ```

4. **Run the web host**

   ```bash
   uv run WebHost.py
   ```

   From there you can fill in options at http://localhost:8080/games/World%20of%20Warcraft/player-options and generate games at http://localhost:8080/generate. Restart the web host to pick up changes to the code.

5. **Set up your editor** (optional)

   Open the `archipelago/worlds/worldofwarcraft` folder in VSCode, copy `.env.example` to `.env`, and uncomment the `PYTHONPATH` line for your OS so that imports from the Archipelago core resolve properly.

## 🤝 Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*May the RNG be with you in your adventures in Azeroth!* ⚔️🐉
