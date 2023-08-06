import backend
import ufl
import ufl.algorithms
import numpy

import fenics_adjoint.types as fenics_types
from pyadjoint.optimization.constraints import Constraint, EqualityConstraint, InequalityConstraint

if backend.__name__ in ["dolfin", "fenics"]:
    import fenics_adjoint.types as backend_types
elif backend.__name__ == "firedrake":
    import firedrake_adjoint.types as backend_types
else:
    raise NotImplementedError("Unknown backend")


def as_vec(x):
    if backend.__name__ in ["dolfin", "fenics"]:
        if isinstance(x, backend.Function):
            out = x.vector().get_local()
        else:
            out = x.get_local()

        if len(out) == 1:
            out = out[0]
        return backend_types.Constant(out)
    elif backend.__name__ == "firedrake":
        with x.dat.vec_ro as vec:
            copy = numpy.array(vec)

        if len(copy) == 1:
            copy = copy[0]
        return fenics_types.Constant(copy)
    else:
        raise NotImplementedError("Unknown backend")


class UFLConstraint(Constraint):
    """
    Easily implement scalar constraints using UFL.

    The form must be a 0-form that depends on a Function control.
    """

    def __init__(self, form, control):

        if not isinstance(control.control, backend.Function):
            raise NotImplementedError("Only implemented for Function controls")

        args = ufl.algorithms.extract_arguments(form)
        if len(args) != 0:
            raise ValueError("Must be a rank-zero form, i.e. a functional")

        u = control.control
        self.V = u.function_space()
        # We want to make a copy of the control purely for use
        # in the constraint, so that our writing it isn't
        # bothering anyone else
        self.u = backend_types.Function(self.V)
        self.form = ufl.replace(form, {u: self.u})

        self.trial = backend.TrialFunction(self.V)
        self.dform = backend.derivative(self.form, self.u, self.trial)
        if len(ufl.algorithms.extract_arguments(ufl.algorithms.expand_derivatives(self.dform))) == 0:
            raise ValueError("Form must depend on control")

        self.test = backend.TestFunction(self.V)
        self.hess = ufl.algorithms.expand_derivatives(backend.derivative(self.dform, self.u, self.test))
        if len(ufl.algorithms.extract_arguments(self.hess)) == 0:
            self.zero_hess = True
        else:
            self.zero_hess = False

    def update_control(self, m):
        if isinstance(m, list):
            assert len(m) == 1
            m = m[0]

        if isinstance(m, backend.Function):
            self.u.assign(m)
        else:
            self.u._ad_assign_numpy(self.u, m, 0)

    def function(self, m):
        self.update_control(m)
        b = backend.assemble(self.form)
        return fenics_types.Constant(b)

    def jacobian(self, m):
        if isinstance(m, list):
            assert len(m) == 1
            m = m[0]

        self.update_control(m)
        out = [backend.assemble(self.dform)]
        return out

    def jacobian_action(self, m, dm, result):
        """Computes the Jacobian action of c(m) in direction dm and stores the result in result. """

        if isinstance(m, list):
            assert len(m) == 1
            m = m[0]
        self.update_control(m)

        form = backend.action(self.dform, dm)
        result.assign(backend.assemble(form))

    def jacobian_adjoint_action(self, m, dp, result):
        """Computes the Jacobian adjoint action of c(m) in direction dp and stores the result in result. """

        if isinstance(m, list):
            assert len(m) == 1
            m = m[0]
        self.update_control(m)

        asm = backend.assemble(dp * ufl.replace(self.dform, {self.trial: self.test}))
        if isinstance(result, backend.Function):
            if backend.__name__ in ["dolfin", "fenics"]:
                result.vector().zero()
                result.vector().axpy(1.0, asm)
            else:
                result.assign(asm)
        else:
            raise NotImplementedError("Do I need to untangle all controls?")

    def hessian_action(self, m, dm, dp, result):
        """Computes the Hessian action of c(m) in direction dm and dp and stores the result in result. """

        if isinstance(m, list):
            assert len(m) == 1
            m = m[0]
        self.update_control(m)

        H = dm * ufl.replace(self.hess, {self.trial: dp})
        if isinstance(result, backend.Function):
            if backend.__name__ in ["dolfin", "fenics"]:
                if self.zero_hess:
                    result.vector().zero()
                else:
                    result.vector().zero()
                    result.vector().axpy(1.0, backend.assemble(H))
            else:
                if self.zero_hess:
                    result.assign(0)
                else:
                    result.assign(backend.assemble(H))
        else:
            raise NotImplementedError("Do I need to untangle all controls?")

    def output_workspace(self):
        """Return an object like the output of c(m) for calculations."""

        return fenics_types.Constant(backend.assemble(self.form))

    def _get_constraint_dim(self):
        """Returns the number of constraint components."""
        return 1


class UFLEqualityConstraint(UFLConstraint, EqualityConstraint):
    pass


class UFLInequalityConstraint(UFLConstraint, InequalityConstraint):
    pass
