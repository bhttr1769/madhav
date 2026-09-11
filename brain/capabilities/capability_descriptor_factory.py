from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.capabilities.models.capability_descriptor_request import (
    CapabilityDescriptorRequest,
)


class CapabilityDescriptorFactory:
    def create(
        self,
        request: CapabilityDescriptorRequest,
    ) -> CapabilityDescriptor:
        if not isinstance(
            request,
            CapabilityDescriptorRequest,
        ):
            raise TypeError(
                "request must be a "
                "CapabilityDescriptorRequest"
            )

        return CapabilityDescriptor(
            id=request.id,
            name=request.name,
            description=request.description,
            version=request.version,
            entry_point=request.entry_point,
            dependencies=request.dependencies,
        )