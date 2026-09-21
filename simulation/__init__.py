"""BNPL agent-based model of the South African consumer credit market.

Implements the 17 submodels specified in `thesis/chapters/02_model.tex` and the 18
decision rules in `scratchpad/DECISIONS.md`.

The model is a counterfactual experiment, not a historical fit: a household population
calibrated to observed 2017 South African conditions, a period in which BNPL was
effectively absent, into which a BNPL lender class is then injected.
"""

from .config import ParamSet, parameter_register
from .model import BNPLModel

__all__ = ["BNPLModel", "ParamSet", "parameter_register"]
