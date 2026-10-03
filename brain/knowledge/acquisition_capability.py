from brain.browser.integrations.browser_knowledge_integrator import (
    BrowserKnowledgeIntegrator,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.manager import BrainManager
from brain.models.document import Document


class AcquisitionCapability:
    """
    Capability entry point for knowledge acquisition.

    Delegates source-specific acquisition to the existing
    acquisition components and preserves Document as the
    canonical output.
    """

    CAPABILITY_ID = "knowledge.acquisition"

    def __init__(
        self,
        browser_integrator: BrowserKnowledgeIntegrator,
        brain_manager: BrainManager,
    ):
        if not isinstance(
            browser_integrator,
            BrowserKnowledgeIntegrator,
        ):
            raise TypeError(
                "browser_integrator must be a "
                "BrowserKnowledgeIntegrator"
            )

        if not isinstance(
            brain_manager,
            BrainManager,
        ):
            raise TypeError(
                "brain_manager must be a BrainManager"
            )

        self._browser_integrator = browser_integrator
        self._brain_manager = brain_manager

    def capability_descriptor(
        self,
    ) -> CapabilityDescriptor:
        return CapabilityDescriptor(
            id=self.CAPABILITY_ID,
            name="Knowledge Acquisition",
            description=(
                "Acquires knowledge from supported "
                "information sources and integrates it "
                "into the existing Document and "
                "knowledge pipeline."
            ),
            version="1.0.0",
            entry_point=(
                "brain.knowledge.acquisition_capability."
                "AcquisitionCapability"
            ),
            dependencies=frozenset(),
        )

    def execute(
        self,
        input_data: object,
    ) -> Document:
        if not isinstance(
            input_data,
            dict,
        ):
            raise TypeError(
                "input_data must be a dict"
            )

        source = input_data.get("source")

        if not isinstance(
            source,
            str,
        ):
            raise TypeError(
                "source must be a string"
            )

        if not source.strip():
            raise ValueError(
                "source must not be empty"
            )

        if source == "browser":
            return self._acquire_browser(
                input_data
            )

        if source == "file":
            return self._acquire_file(
                input_data
            )

        raise ValueError(
            f"unsupported acquisition source: {source}"
        )

    def _acquire_browser(
        self,
        input_data: dict,
    ) -> Document:
        url = input_data.get("url")

        if not isinstance(
            url,
            str,
        ):
            raise TypeError(
                "browser acquisition requires "
                "a string url"
            )

        return self._browser_integrator.learn(
            url
        )

    def _acquire_file(
        self,
        input_data: dict,
    ) -> Document:
        path = input_data.get("path")

        if not isinstance(
            path,
            str,
        ):
            raise TypeError(
                "file acquisition requires "
                "a string path"
            )

        document = self._brain_manager.read(
            path
        )

        return self._brain_manager.learn_document(
            document
        )