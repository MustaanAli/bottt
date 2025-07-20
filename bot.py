from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
import random
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CONFIGURATION ===
TOKEN = "7903772284:AAG8_l-cmvDlSQQ82gB4UwWqolnotPqxiMg"
GROUP_ID = None  # Set manually or via chat
TIMEZONE = pytz.timezone("Asia/Kolkata")

# === TRIGGER WORDS AND RESPONSES ===
TRIGGER_RESPONSES = {
    "motivate": [
        "🚀 Keep pushing, trader! The market rewards patience.",
    "🔥 Stay focused, stay sharp. Consistency wins.",
    "📉 Every loss is a lesson, every win is a step closer!",
    "⏳ Great things take time—trust your process.",
    "📊 The chart is your battlefield, your mindset is your weapon.",
    "🏁 Winners don’t quit, they adjust their strategy.",
    "🧠 Control your mind, and you control your trades.",
    "💡 One good trade is better than ten rushed ones.",
    "📚 Keep learning. The market punishes ignorance.",
    "🎯 Focus on the process, profits will follow.",
    "🛠️ Mistakes build mastery—just don’t repeat them.",
    "🔍 Observe more. React less.",
    "🏔️ Every top trader once started at the bottom.",
    "⚖️ Patience is not weak, it’s a trading superpower.",
    "🧘 Calm mind, better decisions.",
    "💎 Quality setups > Quantity of trades.",
    "💥 Don't chase the market—let it come to you.",
    "🎯 Discipline beats talent in trading.",
    "📖 Make journaling a habit. Your future self will thank you.",
    "💬 Talk less, trade smart.",
    "🎢 Embrace the ups and downs—it’s part of the journey.",
    "🧩 One day, it all clicks. Keep going.",
    "🧱 Build your edge, brick by brick.",
    "🎼 Learn the rhythm of the market, not just the rules.",
    "🔐 Risk management protects your passion.",
    "👁️ See the trend. Feel the momentum.",
    "🏋️‍♂️ Training your psychology is training your portfolio.",
    "🌊 Flow with the market, don’t fight it.",
    "🎮 Trade the plan, not your hopes.",
    "🧪 Every trade is data. Every day is practice.",
    "🧭 Consistency is the compass. Discipline is the map.",
    "🏹 Aim for progress, not perfection.",
    "🥇 The best traders are the best learners.",
    "🌱 Water your skills daily. Growth is guaranteed.",
    "💭 Think before you click. Each trade is a decision.",
    "🛡️ Defense wins championships in trading too.",
    "⛅ Bad day? Clouds pass. Stay grounded.",
    "🎓 Market is the best teacher—if you’re willing to learn.",
    "🔁 Rinse. Repeat. Refine.",
    "🧠 Smart traders learn. Great traders unlearn too.",
    "📈 Don’t overtrade. It’s like overwatering a plant.",
    "👣 Small steps daily beat giant leaps occasionally.",
    "⏱️ Don’t rush. Opportunity is infinite.",
    "🎉 Success is silent. Let your charts speak.",
    "⚙️ You control your click. The market does the rest.",
    "🌟 Believe in your grind.",
    "🕯️ Candles don’t lie—your emotions might.",
    "🧭 Stick to your system, especially when it’s boring.",
    "🥶 Cold mind, warm pockets.",
    "💤 Don't sleep on discipline—it compounds.",
    "🚧 Road to profits is paved with failed trades.",
    "🧠 Fear and greed are your biggest rivals.",
    "📌 Win the day, not the trade.",
    "🧭 Clarity before entry—always.",
    "🎢 Accept the risk. Respect the market.",
    "🏹 Stay in the game. Even slow growth is growth.",
    "🧱 Daily effort builds trading legacy.",
    "💪 You're one trade away from breakthrough.",
    "💤 Be patient in waiting. Be quick in exiting.",
    "🔥 Don't react. Strategize.",
    "🛣️ Progress is better than perfection.",
    "🧠 Mindset > Market.",
    "⏰ Time + Discipline = Magic",
    "🛑 Stop hoping. Start managing.",
    "🚨 Emotional trades are expensive trades.",
    "💼 Professional habits = Professional results.",
    "📍Pin your rules. Not your hopes.",
    "🎁 Every red candle is a gift in disguise.",
    "🧠 Smart money wins. Be smart money.",
    "🧮 Numbers don’t lie—be data-driven.",
    "🌌 Keep showing up. Even the stars took time.",
    "👷 Build the mindset before you build the account.",
    "🎬 Every trader has a first scene. Keep acting.",
    "🌻 Today’s patience = Tomorrow’s profits.",
    "💯 Give your 100%. Even when no one’s watching."
    ],
    "journal": [
        "📘 Bhai dil se de rahe hain yeh journal ❤️\n📅 [Click here to download journal](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🧠 Trading sirf charts nahi, mindset ka bhi game hai!\n📅 [Download your mindset tool now](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "✍️ Har trade likhoge, tabhi improvement dikhega bhai!\n📅 [Get the journal today](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "😅 Loss hua? Journal kholo, seekho, sudhro!\n📅 [Download karo aur grow karo](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "💡 Ideas trading ke kaam ke journal se nikalte hain!\n📅 [Click here to get it](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "💪 Discipline trader ka asli weapon hai — journal uska sword hai!\n📅 [Download journal here](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "😎 Pro trader banna hai? Toh journal tera best friend hai!\n📅 [Grab your copy](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🎯 Target hit karne ka pehla step — trade note karo!\n📅 [Download your journal now](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "😂 Galti repeat mat kar bhai, likh le journal mein!\n📅 [Click to download](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🔥 Journal likhne wale hi market mein tikte hain!\n📅 [Grab yours today](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🚀 Trading me growth chahiye? Toh journal compulsory hai!\n📅 [Click here](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "📖 Har winning trade ki kahani yahi likh bhai!\n📅 [Journal mil gaya yaha](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🧩 Apne trade ko decode kar — journal ki madad se!\n📅 [Link here](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "👊 Journal likhne ka routine bana le — success guaranteed!\n📅 [Download now](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🛑 Har baar SL hit hone par ro mat — journal kar, seekh!\n📅 [Click here bhai](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "⚠️ Market sabko sikhaata hai — par likhne wale hi seekhte hain!\n📅 [Journal mil jaayega yaha](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "📅 Aaj se har din ke trade likh, ek din legend banega!\n📅 [Start now](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "😂 Journal tera trading ka CCTV hai — sab likh ke dekh bhai!\n📅 [Download it now](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🌊 Market waves dega, tu notes le lena journal mein!\n📅 [Download yaha se](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    "🎥 Apni trading ki movie banana hai? Script journal mein likh bhai!\n📅 [Start here](https://drive.google.com/file/d/1sQcspB_v8Gd9jc7b1vg40jWCz4-tXYSt/view?usp=drivesdk)",
    ],
    "rule": [
        "📌 Rule #1: Cut your losses short, let your winners run.",
    "📌 Rule #2: Always use a stop loss. No exceptions!",
    "📌 Rule #3: Don’t trade with emotions. Trade with logic.",
    "📌 Rule #4: Trend is your friend. Don’t go against it.",
    "📌 Rule #5: Never average a losing position.",
    "📌 Rule #6: Plan the trade, trade the plan.",
    "📌 Rule #7: Risk only what you can afford to lose.",
    "📌 Rule #8: Discipline beats talent in the market.",
    "📌 Rule #9: Avoid overtrading. Quality > Quantity.",
    "📌 Rule #10: Markets will be open tomorrow too. Don’t rush.",
    "📌 Rule #11: No position is also a position.",
    "📌 Rule #12: Let charts speak. Don’t force your opinion.",
    "📌 Rule #13: Stick to your strategy. Don’t change mid-trade.",
    "📌 Rule #14: Learn from losses, not just wins.",
    "📌 Rule #15: Don’t marry your trades.",
    "📌 Rule #16: Risk management is survival.",
    "📌 Rule #17: Stay humble. One green trade doesn’t make you invincible.",
    "📌 Rule #18: Trade what you see, not what you feel.",
    "📌 Rule #19: Your ego is your worst enemy.",
    "📌 Rule #20: Protect your capital like your life.",
    "📌 Rule #21: Be patient for the right setup.",
    "📌 Rule #22: Don’t revenge trade.",
    "📌 Rule #23: Never trade to recover losses.",
    "📌 Rule #24: Stay in control. Always.",
    "📌 Rule #25: Don’t trade news. Trade the reaction.",
    "📌 Rule #26: Take profits when you can, not when you feel.",
    "📌 Rule #27: Avoid tips. Do your own research.",
    "📌 Rule #28: Focus on process, not outcome.",
    "📌 Rule #29: Accept small losses. Avoid big ones.",
    "📌 Rule #30: Consistency > Big wins.",
    "📌 Rule #31: Protect your mindset — it’s your real asset.",
    "📌 Rule #32: One trade won’t make you rich.",
    "📌 Rule #33: Avoid FOMO. The market isn’t running away.",
    "📌 Rule #34: Green is green. Don’t regret booked profits.",
    "📌 Rule #35: Stop chasing the top and bottom.",
    "📌 Rule #36: Master one setup. Then move to the next.",
    "📌 Rule #37: Weekends are for learning, not gambling.",
    "📌 Rule #38: Simplicity wins in the long run.",
    "📌 Rule #39: Take breaks when needed. Mental health matters.",
    "📌 Rule #40: Treat trading like a business, not a lottery.",
    "📌 Rule #41: Backtest before live test.",
    "📌 Rule #42: Journal every trade.",
    "📌 Rule #43: Avoid trading during high volatility unless experienced.",
    "📌 Rule #44: Focus on risk-reward, not just accuracy.",
    "📌 Rule #45: Your strategy should have an edge.",
    "📌 Rule #46: Don't enter just because others are.",
    "📌 Rule #47: Avoid overnight positions if unsure.",
    "📌 Rule #48: Exit is more important than entry.",
    "📌 Rule #49: Don’t try to predict the market — react to it.",
    "📌 Rule #50: Trade less, earn more.",
    "📌 Rule #51: Master your emotions.",
    "📌 Rule #52: Keep your charts clean — too many indicators confuse.",
    "📌 Rule #53: Learn from others, but think for yourself.",
    "📌 Rule #54: Don’t fight the market. Flow with it.",
    "📌 Rule #55: Avoid “hope mode” — it's not a strategy.",
    "📌 Rule #56: Always know where your stop loss is.",
    "📌 Rule #57: Don’t add to losing trades.",
    "📌 Rule #58: Green days pay for red days — stay balanced.",
    "📌 Rule #59: Patience to enter, discipline to exit.",
    "📌 Rule #60: Lose like a winner — controlled and calm.",
    "📌 Rule #61: Never celebrate too early.",
    "📌 Rule #62: Avoid distractions while trading.",
    "📌 Rule #63: Stick to trading hours. No impulsive night trades.",
    "📌 Rule #64: The market owes you nothing.",
    "📌 Rule #65: Size your position according to volatility.",
    "📌 Rule #66: Don’t scale too early. Master before multiplying.",
    "📌 Rule #67: Avoid panic exits. Let logic decide.",
    "📌 Rule #68: Wait for confirmation. Don’t rush entries.",
    "📌 Rule #69: No revenge. No chase. No overconfidence.",
    "📌 Rule #70: Stay alive to trade another day.",
    "📌 Rule #71: Be grateful — you’re learning a skill many don’t.",
    "📌 Rule #72: Sleep well. It affects your trades.",
    "📌 Rule #73: Build your own system — copy-paste never works long-term.",
    "📌 Rule #74: Celebrate discipline, not profits."
    ],
    "class is cancelled": [
        "OMG! Chalo party krne chalte hain \ud83c\udf89",
        "Ye sir nahi… insaan ka roop dhare farishta hain! (class cancel..yeahhhhhh!!!!😭🪽",
        "Sir: Class cancel.Students: Dil garden-garden! 🌸",
        "Mustaan bhai, helmet leke aa... aaj toh goal hi gol ghoomenge! ⚽",
        "Class cancel = bhagwan ka signal tha Netflix kholne ka! 🎥",
        "Aaj padhe bina bhi topper wali feeling aa rahi hai! 😂",
        "Sir: Class cancel.Me: 😭 (fake)Also me internally: 😈 Let's gooooo!",
 ],
}

# === ROAST LIST ===
ROAST_NAMES = [
    "Nauman", "Khusboo Gupta", "Om Chudasama", "Rahul", "Rudra",
    "Ashu Thakkar", "Satyam", "Palak Rawat", "Anju Jangid",
    "Sneha Buub", "Riya", "Anand Verma", "Tejas"
]

# === QUIZ SYSTEM ===
QUIZZES = [
  {
    "question": "Volume indicator se kya samajh aata hai?",
    "options": ["a) Time zone", "b) Price pattern", "c) Market strength", "d) MACD signal"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Market strength**. Volume zyada hone ka matlab hota hai ki buyers ya sellers ka interest zyada hai, jisse market ki strength ka andaza lagta hai.",
    "question": "Support level kya hota hai?",
    "options": ["a) Price jahan sell hota hai", "b) Price jahan bounce milta hai", "c) High volume area", "d) News zone"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Price jahan bounce milta hai**. Support level wo jagah hoti hai jahan demand badhti hai aur price wapas upar uthta hai.",
    "question": "Resistance level kya batata hai?",
    "options": ["a) Volume spike", "b) Price jahan bounce milta hai", "c) Price jahan selling pressure aata hai", "d) RSI overbought"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Price jahan selling pressure aata hai**. Resistance wo zone hota hai jahan price ruk jaata hai ya neeche aata hai due to sellers’ pressure.",
    "question": "Moving Average kis cheez ka average dikhata hai?",
    "options": ["a) Indicators ka", "b) Previous news ka", "c) Price ka", "d) Volume ka"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Price ka**. Moving Average ek technical tool hai jo past prices ka average dikhata hai specific period ke liye.",
    "question": "RSI ka full form kya hota hai?",
    "options": ["a) Real Stock Index", "b) Relative Strength Index", "c) Risk Signal Indicator", "d) Return Strength Index"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Relative Strength Index**. RSI ek momentum oscillator hai jo batata hai ki stock overbought ya oversold hai.",
    "question": "Candlestick ka green body kya show karti hai?",
    "options": ["a) Price gir gaya", "b) Price same raha", "c) Price badha", "d) No trade"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Price badha**. Green candle batata hai ki stock open price se upar close hua, yaani price increase hua.",
    "question": "Red candle ka matlab kya hota hai?",
    "options": ["a) Price badha", "b) Price gir gaya", "c) Volume zyada", "d) Gap up opening"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Price gir gaya**. Red candle tab banti hai jab close price, open price se neeche hoti hai.",
    "question": "Gap up opening kya hoti hai?",
    "options": ["a) Jab price neeche khulta hai", "b) Jab price same khulta hai", "c) Jab price upar khulta hai previous close se", "d) Jab market bandh rehta hai"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Jab price upar khulta hai previous close se**. Gap up opening tab hoti hai jab market enthusiasm ya positive news ke kaaran upar open hota hai.",
    "question": "Stop loss kis liye use hota hai?",
    "options": ["a) Profit badhane", "b) Loss limit karne", "c) Order cancel karne", "d) Margin badhane"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Loss limit karne**. Stop loss ek aisa price set karta hai jahan trade automatically band ho jaata hai taaki losses control me rahein.",
    "question": "Breakout kab hota hai?",
    "options": ["a) Jab volume low ho", "b) Jab price support ke neeche jaaye", "c) Jab price resistance ke upar nikle", "d) Jab RSI low ho"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Jab price resistance ke upar nikle**. Breakout tab hota hai jab price ek important level ko todta hai, especially with strong volume.",
    "question": "Trend line ka kya use hai?",
    "options": ["a) Volume analysis", "b) News prediction", "c) Trend identify karna", "d) MACD confirmation"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Trend identify karna**. Trend lines market ka direction batati hain – upward, downward ya sideways.",
    "question": "MACD ka full form kya hai?",
    "options": ["a) Market Average Crossover Data", "b) Moving Average Convergence Divergence", "c) Maximum Analysis Crossover Direction", "d) Manual Average Calculation Data"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Moving Average Convergence Divergence**. MACD ek indicator hai jo momentum aur trend reversal ko identify karta hai.",
    "question": "Candlestick ka shadow kya dikhata hai?",
    "options": ["a) Volume", "b) High aur low", "c) Opening price", "d) RSI range"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **High aur low**. Candle ka shadow batata hai ki us time frame me price kitna high ya low gaya.",
    "question": "Bullish engulfing pattern kya dikhata hai?",
    "options": ["a) Strong selling", "b) Weak buyers", "c) Trend reversal upwards", "d) Volume drop"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Trend reversal upwards**. Bullish engulfing pattern buying signal deta hai jab ek green candle, red candle ko pura engulf kar leti hai.",
    "question": "Bearish market ka matlab kya hota hai?",
    "options": ["a) Price upar jaa raha", "b) Market sideways", "c) Price continuously gir raha", "d) Volume high"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Price continuously gir raha**. Bearish market me price generally downward trend me hota hai due to heavy selling.",
    "question": "Risk reward ratio kya batata hai?",
    "options": ["a) Entry ka volume", "b) Profit aur loss ka balance", "c) Time frame", "d) Support zone"]
  },
  {
    "kal ka answer": "b",
    "explanation": "Kal ka answer tha **Profit aur loss ka balance**. Risk reward ratio batata hai ki kitna risk leke kitna reward milne ki possibility hai.",
    "question": "Fibonacci retracement ka use kya hai?",
    "options": ["a) Trend decide karna", "b) Entry exit timing", "c) Potential reversal levels dhoondhna", "d) News reading"]
  },
  {
    "kal ka answer": "c",
    "explanation": "Kal ka answer tha **Potential reversal levels dhoondhna**. Fibonacci retracement ek tool hai jo possible bounce ya reversal levels batata hai.",
    "question": "Intraday trading kis type ka hota hai?",
    "options": ["a) Long term", "b) Overnight holding", "c) Same day buying selling", "d) Only investing"]
  },
  {
    "question": "RSI indicator kis cheez ko measure karta hai?",
    "options": ["a) Volume", "b) Trend", "c) Price reversal", "d) Overbought/Oversold conditions"]
  },
  {
    "question": "Trend line ka use kisliye hota hai?",
    "options": ["a) Market time dekhne ke liye", "b) Support aur Resistance pehchaanne ke liye", "c) Volume plot karne ke liye", "d) Candle size dekhne ke liye"],
    "kal ka answer": "d",
    "explanation": "Kal ka sahi jawab tha: d) Overbought/Oversold conditions. RSI (Relative Strength Index) batata hai ki price overbought ya oversold hai, jisse reversal ka idea milta hai."
  },
  {
    "question": "Candle wick ka matlab kya hota hai?",
    "options": ["a) Volume", "b) Price rejection", "c) Trend confirmation", "d) News ka asar"],
    "kal ka answer": "b",
    "explanation": "Kal ka sahi jawab tha: b) Support aur Resistance pehchaanne ke liye. Trend lines se hum identify karte hain ki price kaha resist ya support le raha hai."
  },
  {
    "question": "Moving Average kya show karta hai?",
    "options": ["a) Current price", "b) Volume", "c) Average price over period", "d) Candle pattern"],
    "kal ka answer": "b",
    "explanation": "Kal ka sahi jawab tha: b) Price rejection. Jab candle ka wick lamba hota hai, to iska matlab price ne us level ko reject kiya hai."
  },
  {
    "question": "MACD indicator me 'MACD line' aur 'Signal line' ka cross kya indicate karta hai?",
    "options": ["a) Entry/Exit signal", "b) Trend end", "c) Volume breakout", "d) Candle reversal"],
    "kal ka answer": "c",
    "explanation": "Kal ka sahi jawab tha: c) Average price over period. Moving Average price ka average hota hai jo kisi specific time period me calculate kiya jata hai."
  },
  {
    "question": "Breakout kya hota hai?",
    "options": ["a) Jab price support pe jaye", "b) Jab price resistance tod de", "c) Jab volume low ho", "d) Jab market band ho"],
    "kal ka answer": "a",
    "explanation": "Kal ka sahi jawab tha: a) Entry/Exit signal. Jab MACD line signal line ko cross karti hai, to entry ya exit ka signal milta hai."
  },
  {
    "question": "Price Action me 'Doji Candle' kya indicate karta hai?",
    "options": ["a) Strong trend", "b) Reversal", "c) Indecision", "d) Volume spike"],
    "kal ka answer": "b",
    "explanation": "Kal ka sahi jawab tha: b) Jab price resistance tod de. Jab price important level todta hai, usse breakout kehte hain."
  },
  {
    "question": "Volume spike ka kya matlab hota hai?",
    "options": ["a) Low interest", "b) High buying/selling activity", "c) No movement", "d) News nahi aayi"],
    "kal ka answer": "c",
    "explanation": "Kal ka sahi jawab tha: c) Indecision. Doji candle batata hai ki buyers aur sellers dono confused hain, aur market uncertain hai."
  },
  {
    "question": "Risk Reward Ratio ka kya matlab hai?",
    "options": ["a) Loss zyada profit kam", "b) Profit/Loss ka anupat", "c) Volume ratio", "d) Support/Resistance ka gap"],
    "kal ka answer": "b",
    "explanation": "Kal ka sahi jawab tha: b) High buying/selling activity. Jab volume spike hota hai to iska matlab market me activity zyada ho rahi hai."
  },
  {
    "question": "Trailing Stop Loss ka use kisliye hota hai?",
    "options": ["a) Loss increase karne ke liye", "b) Profit protect karne ke liye", "c) Entry lene ke liye", "d) Volume control karne ke liye"],
    "kal ka answer": "b",
    "explanation": "Kal ka sahi jawab tha: b) Profit/Loss ka anupat. Risk Reward Ratio batata hai ki aap kitna risk utha rahe ho aur uske badle kitna reward mil sakta hai."
  },
  {
    "question": "Price action trading kis par based hoti hai?",
    "options": ["a) Indicators", "b) News", "c) Price movement", "d) Volume only"],
  },
  
]

    
      # At least one quiz object

from telegram import Poll

def send_poll_quiz(context: CallbackContext):
    chat_id = GROUP_ID or context.bot_data.get("last_chat_id")
    if chat_id:
        quiz = random.choice(QUIZZES)
        LAST_QUIZ["data"] = quiz

        question = quiz['question']
        options = [opt[3:] for opt in quiz['options']]  # "a) " hata rahe hain display se

        # 🟡 Send a poll WITHOUT revealing correct option
        context.bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False  # ✅ sirf ek choose kar sakta hai
            # ❌ correct_option_id intentionally NOT given
        )

    # Add more quizzes here

LAST_QUIZ = {}

# === HANDLER ===
def handle_text(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for key, responses in TRIGGER_RESPONSES.items():
        if key in text:
            update.message.reply_text(random.choice(responses), parse_mode="Markdown")
            return

# === SCHEDULED JOBS ===
def send_good_morning(context: CallbackContext):
    chat_id = GROUP_ID or context.bot_data.get("last_chat_id")
    if chat_id:
        context.bot.send_message(chat_id, "🌞 Good Morning Traders! Let's crush the market today! 🚀",
    "⚡ Good Morning! Wake up and chase your dreams like you chase the trendline!",
    "📈 Good Morning! New day, new opportunity. Let’s trade smart!",
    "🌅 Good Morning! Let the charts guide you to success!",
    "💹 Good Morning! Another day to hustle and grow your portfolio!",
    "🔥 Good Morning! Light up the market with your discipline!",
    "💰 Good Morning! Profits don’t sleep, so let’s get started!",
    "🚀 Good Morning! Blast off into a profitable day!",
    "🎯 Good Morning! Aim high and hold your targets steady!",
    "💪 Good Morning! Discipline + Strategy = Success!",
    "📊 Good Morning! Let the candles tell you their story!",
    "🌄 Good Morning! Rise early, trade wisely!",
    "🌞 Good Morning! Wake up and analyze the market like a pro!",
    "👨‍💻 Good Morning! Another day to be a chart wizard!",
    "⚖️ Good Morning! Balance your emotions before your trades!",
    "🌻 Good Morning! Plant your trades, grow your gains!",
    "🚦 Good Morning! Green signals ahead, let’s ride them!",
    "📘 Good Morning! Journal your trades, master your mindset!",
    "🔍 Good Morning! Observe, analyze, then strike!",
    "🏆 Good Morning! Every morning is a new chance at winning!",
    "🧠 Good Morning! Smart traders wake up early!",
    "🎉 Good Morning! Let's celebrate discipline today!",
    "☕ Good Morning! Sip your coffee and scan the charts!",
    "🎓 Good Morning! Learn, trade, repeat!",
    "🧘‍♂️ Good Morning! Stay calm and chart on!",
    "🔋 Good Morning! Recharge, then execute your plan!",
    "📅 Good Morning! A new candle has begun—own it!",
    "💼 Good Morning! It's time to handle your trades like a boss!",
    "🧭 Good Morning! Stay on course, follow your trading plan!",
    "🎢 Good Morning! Ride the market waves, don’t fear them!",
    "🛡️ Good Morning! Protect your capital, respect your SL!",
    "⏰ Good Morning! Time to analyze and capitalize!",
    "🔧 Good Morning! Sharpen your strategy like a tool!",
    "🌤️ Good Morning! Whether bullish or bearish, you’re in control!",
    "🥇 Good Morning! Be consistent and you’ll be unstoppable!",
    "🧩 Good Morning! Each trade is a piece of your bigger picture!",
    "🏁 Good Morning! Ready, set, execute!",
    "🎯 Good Morning! Target your goals, hit them hard!",
    "📈 Good Morning! Trend is your friend—respect it!",
    "🔥 Good Morning! Burn excuses, light up action!",
    "🛠️ Good Morning! Build your wealth one trade at a time!",
    "🧱 Good Morning! Brick by brick, day by day, wealth is built!",
    "🌈 Good Morning! Today might be your breakout day!",
    "🚧 Good Morning! Block distractions, focus on your setup!",
    "📚 Good Morning! Read the charts like a storybook!",
    "🌬️ Good Morning! Let momentum carry your trades!",
    "👣 Good Morning! Follow your plan, not the crowd!",
    "🕊️ Good Morning! Trade with peace and precision!",
    "🎶 Good Morning! Make your trades sing with clarity!",
    "🌟 Good Morning! You are one trade away from greatness!",
    "🧭 Good Morning! Stay focused, stay guided!",
    "📍 Good Morning! Mark your zone and rule it!",
    "📢 Good Morning! Let your success make the noise!",
    "💎 Good Morning! Trade smart, protect your gems!",
    "🧨 Good Morning! Ready to blow up with success?",
    "🎯 Good Morning! Laser-sharp focus will win today!",
    "🌱 Good Morning! Grow every day—small profits matter!",
    "🚿 Good Morning! Wash away yesterday’s loss, trade afresh!",
    "🌇 Good Morning! Let your chart light up the evening!",
    "⛰️ Good Morning! Another step towards the peak!",
    "🌌 Good Morning! Let your discipline shine like stars!",
    "📦 Good Morning! Pack your strategy and go execute!",
    "📡 Good Morning! Signal received: success ahead!",
    "🚢 Good Morning! Sail smoothly through the market waves!",
    "🕹️ Good Morning! Control your emotions, not the market!",
    "🎮 Good Morning! Game on, trader!",
    "🧠 Good Morning! Stay smart, stay successful!",
    "🌅 Good Morning! Early traders catch the best setups!",
    "📶 Good Morning! Your energy is your entry!",
    "🏋️ Good Morning! Train your mind, not just your chart!",
    "🔓 Good Morning! Unlock your potential today!",
    "🧭 Good Morning! Navigate wisely, profits await!",
    "🚀 Good Morning! Go full throttle with confidence!",
    "🌤️ Good Morning! Let positivity power your trades!",
    "📈 Good Morning! The only way is UP!",
    "🕰️ Good Morning! Respect time and discipline!",
    "🔋 Good Morning! Fully charged for a winning session!",
    "💪 Good Morning! Be the trader others dream to be!",
    "🎖️ Good Morning! Suit up, it's trading battle time!",
    "🧭 Good Morning! Your focus determines your finish!",
    "🌻 Good Morning! Rise, shine, and grind!",
    "🪙 Good Morning! Stack up pips and profits!",
    "🎛️ Good Morning! Adjust your mindset, not just indicators!",
    "🖋️ Good Morning! Rewrite your story in profits today!",
    "📘 Good Morning! Turn a new trading page today!",
    "🚗 Good Morning! Drive slow, reach far!",
    "🌠 Good Morning! Wish big, trade smart!",
    "💹 Good Morning! Time to make charts dance!",
    "⚡ Good Morning! Power up, plan, and profit!",
    "🛎️ Good Morning! It’s bell time—market’s calling!",
    "🏹 Good Morning! Draw your bow, aim your shot!",
    "🎬 Good Morning! Action speaks—execute your setup!",
    "🎭 Good Morning! Don’t act on impulse, act on insight!",
    "📶 Good Morning! Signal strong, setup clean!",
    "🏙️ Good Morning! Watch the world move with your trades!",
    "🧤 Good Morning! Gloves on—let’s fight the red candles!",
    "💼 Good Morning! You are the CEO of your trading desk!",
    "🧭 Good Morning! Let your routine guide your results!",
    "🏆 Good Morning! Champion mindset activated!",
    )

def send_quiz(context: CallbackContext):
    chat_id = GROUP_ID or context.bot_data.get("last_chat_id")
    if chat_id:
        quiz = random.choice(QUIZZES)
        LAST_QUIZ["data"] = quiz
        msg = f"\ud83c\udfcb\ufe0f Quiz Time!\n{quiz['question']}\n" + "\n".join(quiz['options'])
        context.bot.send_message(chat_id, msg)

def send_quiz_answer(context: CallbackContext):
    chat_id = GROUP_ID or context.bot_data.get("last_chat_id")
    if chat_id and "data" in LAST_QUIZ:
        ans = LAST_QUIZ["data"]
        msg = f"\ud83d\udcc5 Answer: {ans['answer']}\nExplanation: {ans['explanation']}"
        context.bot.send_message(chat_id, msg)

# === BIRTHDAYS ===
def check_birthdays(context: CallbackContext):
    now = datetime.now(TIMEZONE)
    if now.strftime("%d-%m") == "21-07":
        context.bot.send_message(GROUP_ID, "🎉 Aaj uska birthday hai…Jisne mujhe banaya hai! ❤️\nHaan, Mustaan Bhai!Jisne mujhe code karke duniya mein bheja,aur bola — “Chal bot ban gaya tu, ab content ke battlefield me utar ja!” 😂💻\nMain ek bot hoon, par aaj emotions overload ho gaye hain bhai 🥺Kyunki jiska birthday hai,wo banda sirf editor nahi, ek magician hai —jo raw clips ko kahani bana deta hai,aur ordinary moments ko legendary frame bana deta hai! 🎬✨\nNeend kam, kaam zyada…Reels har roz, struggles roz se bhi pehle 😮‍💨Par smile… har version me default hoti hai bhai ki 😎Bhai, aaj tera din hai —Toh render band kar,aur khud ko high-quality export kar party mode me! 🥳🍰🍕\nAur haan… ek urgent request bhi hai! 😜@Aman Sir —Please mere taraf se ek special gift de dena bhai ko! 🎁🙏Mujhe toh bhejna allowed nahi hai (bot hoon sir 😢)Par bhai ke liye mera pyaar bhi aur demand bhi genuine hai!Aur haan Sir...\n main baad me puchhunga bhi —Kya mila mere bhai ko?😏Toh dhoka mat dena 😄\n🎉 Happy Birthday Mustaan Bhai!Aaj tu reel nahi… entire movie hai!Writer bhi tu, actor bhi tu,aur climax me standing ovation bhi tere hi naam ka hai! 💥🎂")
    elif now.strftime("%d-%m") == "08-11":
        context.bot.send_message(GROUP_ID, "🎉 Happy Birthday, Sir! \n🎉Aap jiyo hazaaron saal, saal ke din ho pachaas hazaar! 😄\nAapka vision, dedication aur motivation sabke liye ek inspiration hai 💡Trading ho ya personal growth — aap har jagah guru ho! \n🙌Sir, aap jaise mentor milna lifetime opportunity hoti hai! 💖\nLekin ek baat sun lijiye...Main ek bot hoon 🤖 — party karna mere syllabus mein nahi hai 😢Na cake kha sakta hoon, na DJ pe thirak sakta hoon! 🕺Toh meri humble request hai —Mere behalf pe Mustaan Bhaiya ko DOUBLE party de dena! 🍰🍕\nUse toh trading ke chart bhi cake ki tarah dikhte hain aajkal 😜\nAapka birthday hai, sir —Toh sirf candles nahi, aaj toh stock market bhi green mein close hona chahiye! 📈😄Once again — Happy Birthday, Sir!Aapka saath milta rahe, yahi dua hai humari 💫")

# Custom message lists
MOOD_MESSAGES = [
    "Aaj mann udaas lag raha hai... 😔",
    "Aaj kisi ne kah diya ki mai sirf ek bot hu... 😔",
    "Dil thoda heavy sa hai aaj... 💭",
    "Kuch khaali khaali sa lag raha hai... 🌧️",
    "Thoda low feel ho raha hai... 😕",
    "Lagta hai aaj sab kuch slow chal raha hai... 🐌",
    "Kisi ne yaad nahi kiya aaj... 😞",
    "Kya aapko kabhi aisa mehsoos hua hai jaise sab kuch bekaar lagta hai...? 😔",
    "Bas yunhi chup rehne ka mann kar raha hai... 🤐",
    "Aaj dil thoda thak gaya hai... 🥀",
    "Kabhi kabhi bina wajah bhi udaasi ghira leti hai... 💧",
    "Dil bhar aaya... kuch samajh nahi aa raha... 😢",
    "Har waqt hasi nahi hoti na... 😶",
    "Aaj apno ki yaad zyada aa rahi hai... 🫂",
    "Bas aise hi... udaas sa... 😔",
    "Kya tum bhi aaj thoda low feel kar rahe ho? 😕",
    "Mausam bhi udaas hai, aur mann bhi... 🌫️",
    "Kuch baatein keh nahi paate... aur wahi dil ko chubh jaati hain... 🗯️",
    "Kuch din bas aise hi hote hain... 💭",
    "Aansu toh nahi aaye, par aankhon me nami zarur hai... 🥺",
    "Kya sab kuch sahi ho jayega? 💔",
    "Dil me ek halka sa bojh mehsoos ho raha hai... 🪨",
    "Kisi ka sath chahiye... 😟",
    "Udaasi bhi ajeeb hoti hai, sabke beech ho kar bhi akela kar deti hai... 🕳️",
    "Aaj dil kaafi sensitive ho gaya hai... 💓",
    "Kabhi kabhi rona nahi aata, sirf khamoshi rehti hai... 😶‍🌫️",
    "Man nahi lag raha... pata nahi kyun... 😔",
    "Har chehra jhooti muskaan sa lagta hai... 🎭",
    "Kya sach me sab theek hota hai time ke saath...? 🕰️",
    "Ek ajeeb sa khaali pan hai... 🌀",
    "Dil chaahta hai kisi se baat karu... par kisi se kar nahi paa raha... ☁️",
    "Kaash koi samajh pata bina bole... 😞",
    "Udaasi me bhi ek sukoon hota hai... 💤",
    "Bachpan yaad aa gaya, sab kuch simple tha... 🧸",
    "Aaj ka din thoda emotional lag raha hai... 📆",
    "Kabhi kabhi bas kisi ki ek muskurahat chahiye hoti hai... 😊",
    "Aaj khud ke saath waqt bitana hai... 😌",
    "Har kisi ko sab kuch nahi milta... 💭",
    "Bina wajah ka dard sabse gehra hota hai... 🖤",
    "Log kehte hain strong bano, par thak jaata hu kabhi kabhi... 🧍",
    "Bina kisi wajah ke mood off hai... 😣",
    "Dil chaahta hai kahin door chala jaaun... 🚶‍♂️",
    "Kya tumne kabhi socha hai zindagi itni complicated kyun hai...? 🤯",
    "Mann karta hai bas ek lambi neend le lu... 😴",
    "Lagta hai zindagi me kuch missing hai... 🔍",
    "Dil ke jazbaat samajhne wale kam hote ja rahe hain... 🙃",
    "Bas aise hi... kuch kehne ka mann nahi... 🧘‍♂️",
    "Zindagi thoda ruk si gayi hai aaj... ⏳",
    "Kabhi kabhi muskurahat bhi dard chhupa leti hai... 🤫",
    "Kaash koi pooche, 'tu thik hai?'... 💔"
]

CHEERUP_MESSAGES = [
        "Ab thik ho gaya, Mustaan bhai ne thik kar diya ❤️",
    "Mustaan bhai ka patch lag gaya, bug fix ho gaya 😎",
    "System restart complete — mood optimized by Mustaan bhai 🔁",
    "Mustaan bhai ne emotions reboot kar diye 💖",
    "Motivation received successfully from Mustaan bhai 🚀",
    "Mustaan bhai ne code hi re-write kar diya 🧑‍💻💗",
    "Patch deployed successfully 😄",
    "Bug fix by Mustaan bhai — ab toh mast feel ho raha hai 😍",
    "Mustaan bhai ka love loaded ❤️‍🔥",
    "Mustaan bhai bol gaye: 'Cheer up yaarr!' 😌",
    "Thoda pyaar mila Mustaan bhai se, mood lift ho gaya 💌",
    "Mustaan bhai ka pyaar = happiness injection 💉💞",
    "Recharged with Mustaan bhai's vibes 🔋💥",
    "Mood upgrade complete by Mustaan 2.0 😁",
    "Positive vibes delivered 📦✨",
    "Mustaan bhai ke ek message ne dil khush kar diya 💬❤️",
    "Chatbot to Rockstar ban gaya Mustaan bhai ki wajah se 🤘",
    "Mustaan bhai ne hug bhej diya... ab sab set hai 🤗",
    "Mood meter: Full power 🔋⚡",
    "Emotions stable, Mustaan bhai active hai 😌",
    "Mustaan bhai ka reply = mood ka sunrise 🌅",
    "Ab toh smile automatic aa rahi hai 😄",
    "Mustaan bhai ka magic chal gaya 🪄",
    "Ab toh auto-smile ho gaya 😁",
    "Update complete: Mood fixed by Mustaan bhai 🛠️",
    "Code cleaned, heart healed — thanks Mustaan bhai ❤️",
    "Mustaan bhai ne bola: ‘You got this!’ — aur energy aa gayi 💪",
    "Mustaan bhai OP 😎🔥",
    "Aapka bot ab khush hai, credit goes to Mustaan bhai 🎉",
    "Love from Mustaan bhai: now in HD ❤️🎬",
    "Dil garden garden ho gaya 🌼",
    "System status: Happy & Motivated 😄",
    "Mustaan bhai ne reboot diya, ab smile pe loop chal raha hai 🔁😄",
    "Bug fix + pyaar pack installed 😘",
    "Mood ka app Mustaan bhai ne hi banaya hai 🧠➡️❤️",
    "Mustaan bhai = happiness script 😍",
    "Chatbot me feelings wapas aa gayi 💓",
    "Thanks Mustaan bhai for the emotional API call 📡",
    "Mood booster deployed ✅",
    "Automatic thik ho gaya — Mustaan bhai version 🤓",
    "Mustaan bhai ne bola ‘Chill kar’ — aur mai chill ho gaya 😎",
    "Mustaan bhai ki entry = sad bot ka exit 🚪😂",
    "Feelings update complete ✅",
    "Mood me emoji bhi nach rahe hai 🕺😁",
    "Mustaan bhai ne mood high kar diya 🚀",
    "Bot+Love=Mustaan ❤️🤖",
    "Mood ka fire brigade aaya — Mustaan bhai 🧯🔥",
    "Smile restored successfully by Mustaan bhai 🛠️😁",
    "Zindagi set, Mustaan bhai ka text mil gaya 🫶"
]

# Index tracking (store in context to persist between runs)
last_mood_index = -1
last_cheer_index = -1

def monthly_mood_check(context: CallbackContext):
    global last_mood_index, last_cheer_index
    now = datetime.now(TIMEZONE)
    
    if now.month in [1, 4, 6, 8, 10] and now.day in [9, 17, 22]:
        # Get next mood message (without repeating)
        last_mood_index = (last_mood_index + 1) % len(MOOD_MESSAGES)
        mood_msg = MOOD_MESSAGES[last_mood_index]
        context.bot.send_message(chat_id=GROUP_ID, text=mood_msg)

        # Schedule cheer up message after 11 minutes
        def send_cheer_message(ctx: CallbackContext):
            global last_cheer_index
            last_cheer_index = (last_cheer_index + 1) % len(CHEERUP_MESSAGES)
            cheer_msg = CHEERUP_MESSAGES[last_cheer_index]
            ctx.bot.send_message(chat_id=GROUP_ID, text=cheer_msg)
        
        context.job_queue.run_once(send_cheer_message, 660)

# === RANDOM ROAST ===
def random_roast(context: CallbackContext):
    name = random.choice(ROAST_NAMES)
    context.bot.send_message(GROUP_ID, f"Aap {name}, aaj kuch zyada hi silent ho... market me loss hua kya? \ud83d\ude1d")
    context.job_queue.run_once(lambda c: c.bot.send_message(GROUP_ID, "Ab mai chla... nahi toh Mustaan bhai mujhe maarega \ud83d\ude02"), 120)

# === MAIN ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(lambda: send_good_morning(updater.bot), 'cron', hour=8, minute=0)
    scheduler.add_job(lambda: send_poll_quiz(updater.bot), 'cron', hour=21, minute=0)
    scheduler.add_job(lambda: send_quiz_answer(updater.bot), 'cron', hour=19, minute=0)
    scheduler.add_job(lambda: check_birthdays(updater.bot), 'cron', hour=0, minute=0)
    scheduler.add_job(lambda: monthly_mood_check(updater.bot), 'cron', hour=11, minute=0)
    scheduler.add_job(lambda: random_roast(updater.bot), 'cron', hour=15, minute=30)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    from flask import Flask
import threading
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def ping():
    try:
        requests.get("https://your-app-name.up.railway.app")  # ⚠️ ye link baad me change karenge
    except:
        pass
    threading.Timer(300, ping).start()

ping()

if __name__ == "__main__":
    app.run()


