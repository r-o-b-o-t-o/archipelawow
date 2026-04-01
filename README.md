# 🌍 ArchipelaWoW

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Archipelago](https://img.shields.io/badge/Archipelago-Compatible-green.svg)](https://github.com/ArchipelagoMW/Archipelago)

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

- **Dungeon Completions**: Conquer instances in unexpected orders
- **Achievements**: Unlock feats of glory through randomized paths
- **Flight Paths**: Discover aerial routes across Azeroth as you progress through the zones
- **Experience Gains**: Gaining experience completes checks but doesn't level up your character normally - your actual level stays the same until you receive level-up rewards
- **Quests**: Complete missions in new sequences

### 🎁 Randomized Rewards
- **Items**: Receive powerful gear and artifacts at unexpected times
- **Zone Unlocks**: Access new areas through randomized progression
- **Level Ups**: Increase your character level - these can be sent by other players or by completing location checks

## 🚀 Installation & Usage

### Prerequisites
- [AzerothCore Server](https://www.azerothcore.org/wiki/classic-installation)
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

### Step-by-Step Setup

1. **Install AzerothCore**
   - Follow the [**official installation guide**](https://www.azerothcore.org/wiki/classic-installation)

2. **Add the ArchipelaWoW Module**
   - Add [**`mod-I-found-your-sword`**](https://github.com/r-o-b-o-t-o/mod-i-found-your-sword) to your AzerothCore installation

3. **Install Archipelago**
   - Download and install [**Archipelago**](https://github.com/ArchipelagoMW/Archipelago/releases)

4. **Install the APWorld**
   - Download `azerothcore.apworld` from the [Releases page](https://github.com/r-o-b-o-t-o/archipelawow/releases)
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
   - Edit `archipelawow.conf` in `configs/module`
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
- [Archipelago source installation](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md)

### Setup

1. **Clone the Repository**
   ```bash
   cd archipelago/worlds
   git clone https://github.com/r-o-b-o-t-o/archipelawow.git azerothcore
   ```

2. **Open in VSCode**
   - Open `archipelago/worlds/azerothcore` folder in VSCode
   - Copy `.env.example` to `.env`
   - Configure `PYTHONPATH` in `.env`:
     - Uncomment the appropriate line for your OS
     - Or set: `PYTHONPATH=${PYTHONPATH};C:\absolute\path\to\archipelago`

3. **Build the APWorld**
   ```bash
   # From archipelago directory
   Launcher.py "Build APWorlds" -- "World of Warcraft"
   ```

4. **Host Development Games**
   ```bash
   # From archipelago directory
   python WebHost.py
   ```

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
