"""
Módulo de Verificação de Certificados em Tempo Polinomial.
Demonstração computacional da definição da classe NP:
"Uma linguagem L pertence a NP se, e somente se, existe um verificador determinístico A
em tempo polinomial que atesta a validade de um certificado polinomial c para x ∈ L" (Cormen Cap. 34).
"""

from .verifier import (
    verify_vertex_cover_certificate,
    verify_tsp_certificate,
    VerificationResult,
)

__all__ = [
    "verify_vertex_cover_certificate",
    "verify_tsp_certificate",
    "VerificationResult",
]
