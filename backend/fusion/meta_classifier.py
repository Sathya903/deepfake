class MetaClassifier:

    def fuse(self, scores: dict):

        if not scores:
            return {
                "final_score": 0.0,
                "decision": "Unknown",
                "confidence": 0.0
            }

        # Ensure values are between 0 and 1
        normalized_scores = [
            max(0.0, min(1.0, float(v)))
            for v in scores.values()
        ]

        final_score = sum(normalized_scores) / len(normalized_scores)

        decision = "Fake" if final_score > 0.5 else "Real"

        return {
            "final_score": round(final_score, 3),
            "decision": decision,
            "confidence": round(final_score * 100, 2),
            "model_breakdown": {
                k: round(v * 100, 2) for k, v in scores.items()
            }
        }
