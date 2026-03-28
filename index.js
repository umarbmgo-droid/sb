const { Client } = require('discord.js-selfbot-v13');
const fs = require('fs');
const path = require('path');

// ===== CONFIG =====
const TOKEN = process.env.TOKEN;
const OWNER_ID = "361069640962801664";
const PREFIX = "!";

if (!TOKEN) {
    console.error("❌ ERROR: TOKEN not set in Railway Variables");
    process.exit(1);
}

// ===== CLIENT SETUP =====
const client = new Client({ checkUpdate: false });

// ===== DATA STORAGE =====
let data = {};
const dataFile = path.join(__dirname, 'data.json');

try {
    if (fs.existsSync(dataFile)) {
        data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    }
} catch (e) {
    console.log("No existing data");
}

function saveData() {
    fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
}

// ===== STATUS LOOP =====
async function statusLoop() {
    while (true) {
        await client.user.setActivity("MAR", { type: "STREAMING", url: "https://twitch.tv/mar" });
        await new Promise(resolve => setTimeout(resolve, 30000));
    }
}

// ===== EVENTS =====
client.on('ready', async () => {
    console.log(`✅ SELFBOT ONLINE: ${client.user.tag}`);
    console.log(`🆔 User ID: ${client.user.id}`);
    console.log(`📊 Servers: ${client.guilds.cache.size}`);
    statusLoop();
});

client.on('messageCreate', async (message) => {
    if (message.author.id === client.user.id) return;
    if (!message.content.startsWith(PREFIX)) return;
    if (message.author.id !== OWNER_ID) return;

    const args = message.content.slice(PREFIX.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    await message.delete().catch(() => {});

    switch (command) {
        case 'ping':
            const msg = await message.channel.send(`Pong! ${client.ws.ping}ms`);
            setTimeout(() => msg.delete().catch(() => {}), 3000);
            break;

        case 'status':
            const newStatus = args.join(' ');
            if (!newStatus) {
                const err = await message.channel.send("Usage: !status <text>");
                setTimeout(() => err.delete().catch(() => {}), 3000);
                return;
            }
            await client.user.setActivity(newStatus, { type: "STREAMING", url: "https://twitch.tv/mar" });
            const conf = await message.channel.send(`Status changed to: ${newStatus}`);
            setTimeout(() => conf.delete().catch(() => {}), 3000);
            break;

        case 'stats':
            const statsMsg = await message.channel.send(`Account: ${client.user.tag} | ID: ${client.user.id}`);
            setTimeout(() => statsMsg.delete().catch(() => {}), 5000);
            break;

        default:
            const unknown = await message.channel.send("Unknown command. Use !ping, !status, !stats");
            setTimeout(() => unknown.delete().catch(() => {}), 3000);
    }
});

// ===== RUN =====
console.log("🚀 Starting Selfbot...");
client.login(TOKEN);)
