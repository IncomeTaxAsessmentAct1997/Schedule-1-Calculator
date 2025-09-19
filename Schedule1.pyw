import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
from itertools import combinations_with_replacement, permutations
import copy

class StrandOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule 1 Strand Optimizer")
        self.root.geometry("1200x800")
        
        self.save_file = "strand_optimizer_save.json"
        
        self.strands = {
            "OG Kush": {"price": 38, "base_effect": "Calming"},
            "Sour Diesel": {"price": 40, "base_effect": "Refreshing"},
            "Green Crack": {"price": 43, "base_effect": "Energizing"},
            "Granddaddy Purple": {"price": 44, "base_effect": "Sedating"},
            "Meth": {"price": 70, "base_effect": None},
            "Crack": {"price": 150, "base_effect": None}
        }
        
        self.ingredients = [
            "Cuke", "Banana", "Paracetamol", "Donut", "Viagra", "Mouth Wash", 
            "Flu Medicine", "Gasoline", "Energy Drink", "Motor Oil", "Chili", 
            "Iodine", "Mega Bean", "Addy", "Battery", "Horse Semen"
        ]
        
        self.ingredient_effects = {
            "Cuke": "Energizing",
            "Flu Medicine": "Sedating",
            "Gasoline": "Toxic",
            "Donut": "Calorie-Dense",
            "Energy Drink": "Athletic",
            "Mouth Wash": "Balding",
            "Motor Oil": "Slippery",
            "Banana": "Gingeritis",
            "Chili": "Spicy",
            "Iodine": "Jennerising",
            "Paracetamol": "Sneaky",
            "Viagra": "Tropic Thunder",
            "Mega Bean": "Foggy",
            "Addy": "Thought-Provoking",
            "Battery": "Bright-Eyed",
            "Horse Semen": "Long Faced"
        }
        
        self.advanced_effects = {
            "Cuke": {
                "Toxic": "Euphoric",
                "Slippery": "Munchies",
                "Sneaky": "Paranoia",
                "Foggy": "Cyclopean",
                "Gingeritis": "Thought-Provoking",
                "Munchies": "Athletic",
                "Euphoric": "Laxative"
            },
            "Flu Medicine": {
                "Calming": "Bright-Eyed",
                "Athletic": "Munchies",
                "Thought-Provoking": "Gingeritis",
                "Cyclopean": "Foggy",
                "Munchies": "Slippery",
                "Laxative": "Euphoric",
                "Euphoric": "Toxic",
                "Focused": "Calming",
                "Electrifying": "Refreshing",
                "Shrinking": "Paranoia"
            },
            "Gasoline": {
                "Energizing": "Euphoric",
                "Gingeritis": "Smelly",
                "Jennerising": "Sneaky",
                "Sneaky": "Tropic Thunder",
                "Munchies": "Sedating",
                "Laxative": "Foggy",
                "Disorienting": "Glowing",
                "Paranoia": "Calming",
                "Electrifying": "Disorienting",
                "Shrinking": "Focused"
            },
            "Donut": {
                "Balding": "Sneaky",
                "Anti-Gravity": "Slippery",
                "Jennerising": "Gingeritis",
                "Focused": "Euphoric",
                "Shrinking": "Energizing"
            },
            "Energy Drink": {
                "Sedating": "Munchies",
                "Spicy": "Euphoric",
                "Tropic Thunder": "Sneaky",
                "Glowing": "Disorienting",
                "Foggy": "Laxative",
                "Disorienting": "Electrifying",
                "Schizophrenia": "Balding",
                "Focused": "Shrinking"
            },
            "Mouth Wash": {
                "Calming": "Anti-Gravity",
                "Calorie-Dense": "Sneaky",
                "Explosive": "Sedating",
                "Focused": "Jennerising"
            },
            "Motor Oil": {
                "Energizing": ["Munchies", "Schizophrenia"],
                "Foggy": "Toxic",
                "Euphoric": "Sedating",
                "Paranoia": "Anti-Gravity",
                "Munchies": "Schizophrenia"
            },
            "Banana": {
                "Calming": "Sneaky",
                "Toxic": "Smelly",
                "Long Faced": "Refreshing",
                "Cyclopean": "Thought-Provoking",
                "Disorienting": "Focused",
                "Focused": "Seizure-Inducing",
                "Paranoia": "Jennerising"
            },
            "Chili": {
                "Athletic": "Euphoric",
                "Anti-Gravity": "Tropic Thunder",
                "Sneaky": "Bright-Eyed",
                "Munchies": "Toxic",
                "Laxative": "Long Faced",
                "Shrinking": "Refreshing"
            },
            "Iodine": {
                "Calming": "Balding",
                "Toxic": "Sneaky",
                "Foggy": "Paranoia",
                "Calorie-Dense": "Gingeritis",
                "Euphoric": "Seizure-Inducing",
                "Refreshing": "Thought-Provoking"
            },
            "Paracetamol": {
                "Calming": "Slippery",
                "Toxic": "Tropic Thunder",
                "Spicy": "Bright-Eyed",
                "Glowing": "Toxic",
                "Foggy": "Calming",
                "Munchies": "Anti-Gravity",
                "Electrifying": "Athletic"
            },
            "Viagra": {
                "Athletic": "Sneaky",
                "Euphoric": "Bright-Eyed",
                "Laxative": "Calming",
                "Disorienting": "Toxic"
            },
            "Mega Bean": {
                "Calming": "Glowing",
                "Sneaky": ["Calming", "Glowing"],
                "Jennerising": "Paranoia",
                "Athletic": "Laxative",
                "Slippery": "Toxic",
                "Thought-Provoking": ["Energizing", "Cyclopean"],
                "Seizure-Inducing": "Focused",
                "Focused": "Disorienting",
                "Shrinking": "Electrifying"
            },
            "Addy": {
                "Sedating": "Gingeritis",
                "Long Faced": "Electrifying",
                "Glowing": "Refreshing",
                "Foggy": "Energizing",
                "Explosive": "Euphoric"
            },
            "Battery": {
                "Munchies": "Tropic Thunder",
                "Laxative": "Calorie-Dense",
                "Electrifying": "Euphoric",
                "Shrinking": "Munchies"
            },
            "Horse Semen": {
                "Anti-Gravity": "Calming",
                "Gingeritis": "Refreshing",
                "Thought-Provoking": "Electrifying"
            }
        }
        
        self.special_conditions = {
            "Banana": {"Energizing": {"condition": "no Cyclopean", "result": "Thought-Provoking"}},
            "Paracetamol": {
                "Energizing": [
                    {"condition": "no Munchies", "result": "Paranoia"},
                    {"condition": "with Paranoia", "result": "Balding"}
                ]
            },
            "Donut": {"Calorie-Dense": {"condition": "no Explosive", "result": "add Explosive"}},
            "Mega Bean": {
                "Energizing": {"condition": "no Thought-Provoking", "result": "Cyclopean"}
            },
            "Battery": {
                "Euphoric": [
                    {"condition": "no Electrifying", "result": "Zombifying"},
                    {"condition": "no Zombifying", "result": "Euphoric"}
                ]
            }
        }
        
        self.effect_values = {
            "Shrinking": 1.60, "Zombifying": 1.58, "Cyclopean": 1.56, "Anti-Gravity": 1.54,
            "Long Faced": 1.52, "Electrifying": 1.50, "Glowing": 1.48, "Tropic Thunder": 1.46,
            "Thought-Provoking": 1.44, "Jennerising": 1.42, "Bright-Eyed": 1.40, "Spicy": 1.38,
            "Foggy": 1.36, "Slippery": 1.34, "Athletic": 1.32, "Balding": 1.30,
            "Calorie-Dense": 1.28, "Sedating": 1.26, "Sneaky": 1.24, "Energizing": 1.22,
            "Gingeritis": 1.20, "Euphoric": 1.18, "Focused": 1.16, "Refreshing": 1.14,
            "Munchies": 1.12, "Calming": 1.10, "Explosive": 1.00, "Lethal": 1.00,
            "Disorienting": 1.00, "Laxative": 1.00, "Paranoia": 1.00, "Schizophrenic": 1.00,
            "Seizure-Inducing": 1.00, "Smelly": 1.00, "Toxic": 1.00
        }
        
        self.available_ingredients = {}
        self.available_strands = {}
        self.calculation_count = 0
        self.max_calculations = 50000
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(left_frame, text="Available Strands:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        strands_frame = ttk.Frame(left_frame)
        strands_frame.pack(fill=tk.X, pady=(0, 10))
        
        for strand in self.strands.keys():
            var = tk.BooleanVar()
            self.available_strands[strand] = var
            cb = ttk.Checkbutton(strands_frame, text=f"{strand} (${self.strands[strand]['price']})", 
                               variable=var, command=self.save_settings)
            cb.pack(anchor=tk.W)
        
        ttk.Label(left_frame, text="Available Ingredients:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        ingredients_frame = ttk.Frame(left_frame)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(ingredients_frame)
        scrollbar = ttk.Scrollbar(ingredients_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for ingredient in self.ingredients:
            var = tk.BooleanVar()
            self.available_ingredients[ingredient] = var
            cb = ttk.Checkbutton(scrollable_frame, text=ingredient, variable=var, command=self.save_settings)
            cb.pack(anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(control_frame, text="Find Best Strand", command=self.find_best_strand).pack(pady=10)
        
        ttk.Label(right_frame, text="Results:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(right_frame, width=60, height=30, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def save_settings(self):
        settings = {
            "strands": {name: var.get() for name, var in self.available_strands.items()},
            "ingredients": {name: var.get() for name, var in self.available_ingredients.items()}
        }
        with open(self.save_file, 'w') as f:
            json.dump(settings, f)
    
    def load_settings(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    settings = json.load(f)
                    for name, value in settings.get("strands", {}).items():
                        if name in self.available_strands:
                            self.available_strands[name].set(value)
                    for name, value in settings.get("ingredients", {}).items():
                        if name in self.available_ingredients:
                            self.available_ingredients[name].set(value)
            except:
                pass
    
    def apply_effects(self, current_effects, ingredient):
        effects_to_add = []
        effects_to_remove = []
        
        base_effect = self.ingredient_effects.get(ingredient)
        if base_effect:
            effects_to_add.append(base_effect)
        
        if ingredient in self.advanced_effects:
            for existing_effect in current_effects:
                if existing_effect in self.advanced_effects[ingredient]:
                    replacement = self.advanced_effects[ingredient][existing_effect]
                    
                    if ingredient == "Motor Oil" and existing_effect == "Energizing":
                        effects_to_remove.append(existing_effect)
                        effects_to_add.extend(["Munchies", "Schizophrenia"])
                    elif ingredient == "Mega Bean" and existing_effect == "Sneaky":
                        effects_to_remove.append(existing_effect)
                        effects_to_add.extend(["Calming", "Glowing"])
                    elif ingredient == "Mega Bean" and existing_effect == "Thought-Provoking":
                        effects_to_remove.append(existing_effect)
                        effects_to_add.extend(["Energizing", "Cyclopean"])
                    elif isinstance(replacement, list):
                        effects_to_remove.append(existing_effect)
                        effects_to_add.extend(replacement)
                    else:
                        effects_to_remove.append(existing_effect)
                        effects_to_add.append(replacement)
        
        if ingredient in self.special_conditions:
            for effect, conditions in self.special_conditions[ingredient].items():
                if effect in current_effects:
                    if isinstance(conditions, list):
                        for condition in conditions:
                            if self.check_condition(current_effects, condition):
                                if condition["result"] == "Balding" and effect == "Energizing":
                                    if "Paranoia" in current_effects:
                                        effects_to_remove.extend(["Energizing", "Paranoia"])
                                        effects_to_add.append("Balding")
                                elif condition["result"] != "add Explosive":
                                    effects_to_remove.append(effect)
                                    effects_to_add.append(condition["result"])
                    else:
                        if self.check_condition(current_effects, conditions):
                            if conditions["result"] == "add Explosive":
                                effects_to_add.append("Explosive")
                            else:
                                effects_to_remove.append(effect)
                                effects_to_add.append(conditions["result"])
        
        new_effects = [e for e in current_effects if e not in effects_to_remove]
        new_effects.extend(effects_to_add)
        
        new_effects = list(dict.fromkeys(new_effects))
        
        return new_effects[:8]
    
    def check_condition(self, current_effects, condition):
        if condition["condition"] == "no Cyclopean":
            return "Cyclopean" not in current_effects
        elif condition["condition"] == "no Munchies":
            return "Munchies" not in current_effects
        elif condition["condition"] == "with Paranoia":
            return "Paranoia" in current_effects
        elif condition["condition"] == "no Explosive":
            return "Explosive" not in current_effects
        elif condition["condition"] == "no Thought-Provoking":
            return "Thought-Provoking" not in current_effects
        elif condition["condition"] == "no Electrifying":
            return "Electrifying" not in current_effects
        elif condition["condition"] == "no Zombifying":
            return "Zombifying" not in current_effects
        return False
    
    def calculate_strand_value(self, strand_name, recipe):
        base_price = self.strands[strand_name]["price"]
        effects = []
        
        if self.strands[strand_name]["base_effect"]:
            effects.append(self.strands[strand_name]["base_effect"])
        
        for ingredient in recipe:
            effects = self.apply_effects(effects, ingredient)
            if len(effects) >= 8:
                break
        
        multipliers = [self.effect_values.get(effect, 1.0) - 1.0 for effect in effects]
        total_multiplier = sum(multipliers)
        final_price = base_price * (1 + total_multiplier)
        
        return round(final_price), effects, recipe
    
    def find_best_strand(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Calculating best strand...\n\n")
        self.root.update()
        
        available_strands = [name for name, var in self.available_strands.items() if var.get()]
        available_ingredients = [name for name, var in self.available_ingredients.items() if var.get()]
        
        if not available_strands:
            self.result_text.insert(tk.END, "Please select at least one strand.\n")
            return
        
        if not available_ingredients:
            self.result_text.insert(tk.END, "Please select at least one ingredient.\n")
            return
        
        best_value = 0
        best_strand = None
        best_effects = []
        best_recipe = []
        
        self.calculation_count = 0
        
        for strand in available_strands:
            for recipe_length in range(1, 9):
                if self.calculation_count >= self.max_calculations:
                    break
                
                for recipe_combo in combinations_with_replacement(available_ingredients, recipe_length):
                    if self.calculation_count >= self.max_calculations:
                        break
                    
                    for recipe in set(permutations(recipe_combo)):
                        if self.calculation_count >= self.max_calculations:
                            break
                        
                        self.calculation_count += 1
                        
                        try:
                            value, effects, full_recipe = self.calculate_strand_value(strand, recipe)
                            
                            if value > best_value:
                                best_value = value
                                best_strand = strand
                                best_effects = effects
                                best_recipe = full_recipe
                        except Exception as e:
                            continue
                
                if self.calculation_count >= self.max_calculations:
                    break
            
            if self.calculation_count >= self.max_calculations:
                break
        
        self.result_text.delete(1.0, tk.END)
        
        if best_strand:
            self.result_text.insert(tk.END, f"BEST STRAND FOUND:\n")
            self.result_text.insert(tk.END, f"=" * 50 + "\n\n")
            self.result_text.insert(tk.END, f"Base Strand: {best_strand} (${self.strands[best_strand]['price']})\n")
            self.result_text.insert(tk.END, f"Final Value: ${best_value}\n\n")
            
            self.result_text.insert(tk.END, f"Recipe Steps:\n")
            base_price = self.strands[best_strand]["price"]
            current_effects = []
            if self.strands[best_strand]["base_effect"]:
                current_effects.append(self.strands[best_strand]["base_effect"])
                self.result_text.insert(tk.END, f"Start with base effect: {self.strands[best_strand]['base_effect']}\n")
            
            for i, ingredient in enumerate(best_recipe, 1):
                self.result_text.insert(tk.END, f"{i}. Add {ingredient}\n")
                current_effects = self.apply_effects(current_effects, ingredient)
            
            self.result_text.insert(tk.END, f"\nFinal Effects: {', '.join(best_effects)}\n")
            
            multipliers = [self.effect_values.get(effect, 1.0) - 1.0 for effect in best_effects]
            self.result_text.insert(tk.END, f"Effect Multipliers: {[f'{m:.2f}' for m in multipliers]}\n")
            self.result_text.insert(tk.END, f"Total Multiplier: {sum(multipliers):.2f}\n")
            self.result_text.insert(tk.END, f"Calculation: {base_price} * (1 + {sum(multipliers):.2f}) = ${best_value}\n")
            
        else:
            self.result_text.insert(tk.END, "No valid strands found with current selections.\n")
        
        self.result_text.insert(tk.END, f"\nCalculations performed: {self.calculation_count:,}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = StrandOptimizer(root)
    root.mainloop()