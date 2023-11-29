from dataclasses import dataclass, field
from typing import Optional, Union

from typetemp.template.typed_prompt import TypedPrompt


@dataclass
class TypedPitchMessagePrompt(TypedPrompt):
    """
    TypedPitchMessagePrompt Class Description:
    -----------------------------------------------------------
    This class generates a two-sentence pitch aimed at Chiefs of Staff in billionaire multi-family offices.
    It inherits from TypedPrompt for leveraging its template rendering capabilities.

    Attributes:
    -----------------------------------------------------------
    - pitch_message: The generated pitch message.
    - source: The generic template string for generating the pitch.
    - sys_msg: System message to describe the AI assistant's role.

    Methods:
    -----------------------------------------------------------
    __call__: Inherits the __call__ method from TypedPrompt for output generation.
    """

    pitch_message: Optional[str] = None  # Generated pitch message
    source: str = (
        "As a leader in tech solutions for multi-family offices, I can bring unparalleled efficiency to your operations. "
        "Would you be interested in a free consultation to explore how we can elevate your asset management strategies?"
    )
    sys_msg: str = "You are a pitch message generation AI assistant."

    def __call__(self, **kwargs) -> Union[str, Optional[str]]:
        """
        __call__ Method Description:
        -----------------------------------------------------------
        This method uses TypedPrompt's __call__ method to generate the pitch message.

        Parameters:
        -----------------------------------------------------------
        **kwargs: Optional keyword arguments for template rendering.

        Returns:
        -----------------------------------------------------------
        Union[str, Optional[str]]: The generated pitch message.
        """

        self.pitch_message = super().__call__(
            **kwargs
        )  # Invoke TypedPrompt's call method

        if self.to == "stdout":
            print(
                self.pitch_message
            )  # Print the pitch message if stdout is the chosen output medium

        return self.pitch_message  # Return the generated pitch message


if __name__ == "__main__":
    # Create an instance of TypedPitchMessagePrompt class
    pitch_prompt = TypedPitchMessagePrompt(to="stdout")

    # Generate and output the pitch message
    pitch_prompt()
