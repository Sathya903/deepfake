class MetaClassifier:

    def __init__(self):
        self.weights = {
            "cnn": 0.4,
            "frequency": 0.3,
            "landmark": 0.3,
            "frame_model": 0.5,
            "temporal_model": 0.5,
            "spectrogram": 0.5,
            "mfcc": 0.5
        }

    def fuse(self, scores: dict):

        total_score = 0
        total_weight = 0

        for key, value in scores.items():
            weight = self.weights.get(key, 0.3)
            total_score += value * weight
            total_weight += weight

        if total_weight == 0:
            final_score = 0
        else:
            final_score = total_score / total_weight

        decision = "Fake" if final_score > 0.5 else "Real"

        return {
            "final_score": round(final_score, 3),
            "decision": decision
        }
