import pandas as pd
import difflib

class ManualSymptomChecker:
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)
        self.data['symptoms'] = self.data['symptoms'].str.lower()
        self.data['diagnosis'] = self.data['diagnosis'].fillna("No diagnosis provided.")
        self.data['home_remedy'] = self.data.get('home_remedy', pd.Series(["No remedy available."] * len(self.data)))

    def _tokenize(self, text):
        # Splits text by comma and whitespace to create a set of symptom keywords
        return set(word.strip() for part in text.lower().split(',') for word in part.strip().split())

    def _fuzzy_match_score(self, input_words, row_symptoms):
        total_score = 0
        max_score = len(row_symptoms)

        for sym in row_symptoms:
            best_similarity = 0
            for word in input_words:
                similarity = difflib.SequenceMatcher(None, word, sym).ratio()
                if similarity > best_similarity:
                    best_similarity = similarity
            total_score += best_similarity  # Add the best similarity for each symptom

        return total_score, max_score  # Return total score and max score for normalization

    def predict(self, symptoms_input):
        input_words = self._tokenize(symptoms_input)

        best_match_row = None
        best_confidence = 0

        for _, row in self.data.iterrows():
            row_symptoms = self._tokenize(row['symptoms'])
            score, max_score = self._fuzzy_match_score(input_words, row_symptoms)

            confidence = (score / max_score) * 100 if max_score else 0

            if confidence > best_confidence:
                best_confidence = confidence
                best_match_row = row

        if best_match_row is not None and best_confidence > 0:
            diagnosis = best_match_row['diagnosis'].strip().title()
            remedy = best_match_row.get("home_remedy", "No remedy available.").strip()

            return (
                f"⚠️ *This tool is for informational use only and not a substitute for professional medical advice.*\n\n"
                f"🔍 Based on your symptoms, a possible condition might be:\n"
                f"🩺 {diagnosis}\n"
                f"📊 Match Confidence: {best_confidence:.1f}%\n\n"
                f"💡 Suggested Home Remedy:\n"
                f"🫖 {remedy}"
            )
        else:
            return (
                f"⚠️ *This tool is for informational use only and not a substitute for professional medical advice.*\n\n"
                f"😕 No clear match found.\nPlease describe your symptoms more clearly or consult a medical professional."
            )
