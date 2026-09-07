from dataclasses import dataclass

from .traits import ProcessTraits, ProcessTraitAnalyzer


@dataclass
class ProcessClassification:

    category: str

    traits: ProcessTraits

    confidence: float = 1.0


class ProcessClassifier:

    def __init__(self):

        self.trait_analyzer = ProcessTraitAnalyzer()

    def classify(self, process):

        traits = self.trait_analyzer.analyze(process)

        category = self._determine_category(process, traits)

        confidence = self._calculate_confidence(process, traits, category)

        return ProcessClassification(
            category=category, traits=traits, confidence=confidence
        )

    def _determine_category(self, process, traits):

        name = (process.name or "").lower()

        if traits.network_active and traits.long_running:
            return "network_service"

        if traits.cpu_intensive and traits.multi_threaded:
            return "industrial"

        if traits.storage_active:

            if traits.cpu_intensive:
                return "industrial"

            return "storage_service"

        interactive_names = {
            "chrome",
            "firefox",
            "edge",
            "explorer",
            "code",
            "code.exe",
            "claude",
        }

        if name in interactive_names:
            return "commercial"

        if traits.infrastructure_like:
            return "infrastructure"

        if traits.short_lived:
            return "temporary"

        return "generic"

    def _calculate_confidence(self, process, traits, category):

        score = 0.5

        if category == "network_service":
            if traits.network_active:
                score += 0.2

            if traits.long_running:
                score += 0.2

        elif category == "industrial":

            if traits.cpu_intensive:
                score += 0.2

            if traits.multi_threaded:
                score += 0.2

        elif category == "storage_service":

            if traits.storage_active:
                score += 0.3

        elif category == "infrastructure":

            if traits.background:
                score += 0.2

            if traits.long_running:
                score += 0.2

        return min(score, 1.0)
