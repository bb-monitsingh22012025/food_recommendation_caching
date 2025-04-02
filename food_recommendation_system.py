import aerospike
import hashlib
import tkinter as tk
from tkinter import messagebox
from huggingface_hub import InferenceClient  # ✅ Using Hugging Face API

# Initialize Hugging Face API Client
HUGGINGFACE_API_TOKEN = "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"  # Replace with your actual token
hf_client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=HUGGINGFACE_API_TOKEN)

# Aerospike Configuration
aero_config = {'hosts': [('127.0.0.1', 3000)]}
aero_client = aerospike.client(aero_config).connect()

namespace = "test"
set_name = "food_recommendations"

# 🔹 Function to Hash Queries
def hash_query(query):
    return hashlib.sha256(query.lower().encode()).hexdigest()

# 🔹 Check if the Query Exists in Aerospike (Cache)
def check_cache(query):
    hashed_key = hash_query(query)
    key = (namespace, set_name, hashed_key)

    try:
        (_, _, record) = aero_client.get(key)
        print("✅ Cache Hit! Returning stored recommendation.")
        return record["recommendation"]
    except aerospike.exception.RecordNotFound:
        print("❌ Cache Miss! Fetching recommendation from Hugging Face API.")
        return None
    except Exception as e:
        print(f"⚠️ Aerospike Error: {e}")
        return None

# 🔹 Store Response in Aerospike for Future Use
def store_in_cache(query, recommendation):
    hashed_key = hash_query(query)
    key = (namespace, set_name, hashed_key)

    try:
        aero_client.put(key, {"query": query, "recommendation": recommendation})
        (_, _, record) = aero_client.get(key)  # Verify Storage
        print(f"✅ Verified Storage: {record['recommendation']}")
    except Exception as e:
        print(f"⚠️ Error Storing in Cache: {e}")

# 🔹 Generate Recommendation using Hugging Face API
def get_mistral_recommendation(query):
    try:
        response = hf_client.text_generation(prompt=query, max_new_tokens=900).strip()

        # Ensure response is valid
        if not response or len(response) < 5:
            return "Sorry, I couldn't generate a meaningful recommendation."

        return response
    except Exception as e:
        print(f"⚠️ Hugging Face API Error: {e}")
        return "Error: Unable to generate recommendation."

# 🔹 Get Food Recommendation (Main Logic)
def get_food_recommendation():
    user_query = query_entry.get().strip()

    if not user_query:
        messagebox.showwarning("Input Error", "Please enter a food query.")
        return

    # 1️⃣ Check Cache
    cached_response = check_cache(user_query)
    if cached_response:
        print(f"✅ Using Cached Recommendation: {cached_response}")  
        recommendation_label.config(text=f"Recommendation:\n{cached_response}")
        root.update_idletasks()  # Force GUI update
        return

    # 2️⃣ Query Hugging Face API if not found in cache
    mistral_response = get_mistral_recommendation(user_query)

    # 3️⃣ Store Response in Cache
    store_in_cache(user_query, mistral_response)

    # 4️⃣ Display Recommendation in GUI
    recommendation_label.config(text=f"Recommendation:\n{mistral_response}")
    root.update_idletasks()

# 🔹 GUI Setup with Tkinter
root = tk.Tk()
root.title("Food Recommendation System")
root.geometry("500x400")

# UI Components
tk.Label(root, text="Enter Food Query:", font=("Arial", 12)).pack(pady=5)
query_entry = tk.Entry(root, width=50, font=("Arial", 12))
query_entry.pack(pady=5)

get_recommendation_button = tk.Button(
    root, text="Get Recommendation", command=get_food_recommendation,
    font=("Arial", 12), bg="blue", fg="white"
)
get_recommendation_button.pack(pady=10)

recommendation_label = tk.Label(root, text="", wraplength=450, font=("Arial", 12), justify="left")
recommendation_label.pack(pady=10)

# Run GUI
root.mainloop()

# Close Aerospike Connection on Exit
aero_client.close()