# Example Videos

Here are examples showing the range of explainer videos you can create with prompt2production.

## 🔧 Technology Explainers

### How Docker Works
```bash
python create_video.py "how docker technology works"
```

**Generated Script Preview:**
> Docker is a technology that packages applications into containers. Think of it like shipping containers for software. Each container includes everything the app needs to run: code, libraries, and settings. This makes applications portable across different systems...

**Visual Style:** Modern tech workspace, animated containers, clean blue palette

---

### How Bitcoin Works
```bash
python create_video.py "how bitcoin cryptocurrency works" --metaphor "digital gold rush"
```

**Generated Script Preview:**
> Bitcoin is a digital currency that operates without central banks. Like gold miners verifying precious metal, network participants verify transactions. Each transaction is recorded in a public ledger called the blockchain...

**Visual Style:** Gold rush imagery transitioning to digital networks

---

## 🧬 Science Topics

### How Photosynthesis Works
```bash
python create_video.py "how photosynthesis works in plants"
```

**Generated Script Preview:**
> Photosynthesis is how plants convert sunlight into food. Inside leaf cells, chloroplasts capture light energy. This energy splits water molecules and combines carbon dioxide to create glucose...

**Visual Style:** Macro views of leaves, cellular animations, green palette

---

### How Vaccines Work
```bash
python create_video.py "how vaccines train the immune system" --voice british-female
```

**Generated Script Preview:**
> Vaccines teach your immune system to recognize threats. They contain weakened or inactive parts of a disease-causing organism. Your body learns to produce antibodies without getting sick...

**Visual Style:** Medical animations, antibody illustrations, clinical aesthetic

---

## 🌐 Internet & Computing

### How WiFi Works
```bash
python create_video.py "how wifi wireless internet works" --metaphor "radio waves"
```

**Generated Script Preview:**
> WiFi uses radio waves to transmit data through the air. Your router broadcasts signals like a radio station. Devices tune in to specific frequencies to send and receive information...

**Visual Style:** Radio wave visualizations, home router setup, signal propagation

---

### How Search Engines Work
```bash
python create_video.py "how google search finds web pages" --duration 60
```

**Generated Script Preview:**
> Search engines explore the web like digital librarians. Web crawlers visit billions of pages, following links to discover content. These pages are indexed and ranked by relevance...

**Visual Style:** Spider web of connections, library metaphor, data centers

---

## 🎨 Creative Examples

### With Playful Tone
```bash
python create_video.py "how pizza delivery apps work" \
  --voice playful \
  --style "fun and energetic"
```

**Generated Script Preview:**
> Ever wonder how that pizza magically appears at your door? Your order zooms through the internet to the restaurant. GPS tracks your driver like a delicious treasure map...

**Visual Style:** Cartoon pizza journey, colorful app interfaces, happy animations

---

### With Professional Tone
```bash
python create_video.py "how supply chain management works" \
  --voice professional \
  --style "corporate training"
```

**Generated Script Preview:**
> Supply chain management orchestrates the flow of goods from manufacturers to consumers. It coordinates suppliers, warehouses, and transportation networks to optimize efficiency...

**Visual Style:** Corporate infographics, warehouse footage, flowchart animations

---

## 🎯 Different Durations

### Quick 30-Second Explainer
```bash
python create_video.py "how qr codes work" --duration 30 --segment 3
```
- 10 segments × 3 seconds each
- ~75 words total
- Rapid, focused explanation

### Detailed 60-Second Deep Dive
```bash
python create_video.py "how neural networks learn" --duration 60 --segment 5
```
- 12 segments × 5 seconds each
- ~150 words total
- More comprehensive coverage

---

## 🗣️ Voice Variations

### Morgan Freeman Style
```bash
python create_video.py "how the universe began" --voice morgan-freeman
```

### David Attenborough Style
```bash
python create_video.py "how coral reefs form" --voice david-attenborough
```

### Energetic Teacher
```bash
python create_video.py "how multiplication works" --voice enthusiastic-teacher
```

---

## 💡 Using Metaphors Effectively

### Technical Topic with Everyday Metaphor
```bash
python create_video.py "how kubernetes orchestrates containers" \
  --metaphor "orchestra conductor directing musicians"
```

### Abstract Concept with Visual Metaphor
```bash
python create_video.py "how encryption protects data" \
  --metaphor "secret decoder rings and locked safes"
```

### Business Process with Familiar Metaphor
```bash
python create_video.py "how venture capital funding works" \
  --metaphor "dragon's den investment show"
```

---

## 📊 Example Output Structure

Every video generates these files:

```
output/video_20240115_143022/
├── final_video.mp4          # Your complete 45-second video
├── full_script.txt          # "Docker is a technology that..."
├── segment_breakdown.txt    # [00-05s] "Docker is a technology..."
├── storyboard.md           # Scene 1: Wide shot of tech workspace...
├── narration.mp3           # Complete voice-over audio
├── metadata.json           # {"duration": 45, "segments": 9, ...}
└── segments/               # Individual 5-second video clips
    ├── segment_01.mp4
    ├── segment_02.mp4
    └── ...
```

---

## 🚀 Pro Tips

1. **Start simple** - Test with well-known topics first
2. **Metaphors help** - They create more engaging visuals
3. **Keep it focused** - One main concept per video
4. **Natural language** - Write topics like you'd ask a friend
5. **Iterate** - Generate multiple versions to find the best explanation

---

## 🎬 Ready to Create?

Pick any topic you want to explain and try it:

```bash
python create_video.py "how [YOUR TOPIC] works"
```

The AI will handle the rest!