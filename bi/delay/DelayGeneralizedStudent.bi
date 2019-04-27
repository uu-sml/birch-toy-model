/*
 * Delayed Generalized Student's $t$ random variate.
 */
final class DelayGeneralizedStudent(x:Random<Real>&, ν:Real, μ:Real, σ2:Real) < DelayValue<Real>(x) {
  /**
   * Degrees of freedom.
   */
  ν:Real <- ν;

  /**
   * Location parameter.
   */
  μ:Real <- μ;

  /**
   * Squared scale parameter.
   */
  σ2:Real <- σ2;
  
  function simulate() -> Real {
    return simulate_student_t(ν, μ, σ2);
  }
  
  function observe(x:Real) -> Real {
    return observe_student_t(x, ν, μ, σ2);
  }

  function update(x:Real) {
    //
  }

  function downdate(x:Real) {
    //
  }

  function pdf(x:Real) -> Real {
    return pdf_student_t(x, ν, μ, σ2);
  }

  function cdf(x:Real) -> Real {
    return cdf_student_t(x, ν, μ, σ2);
  }

  function write(buffer:Buffer) {
    prune();
    buffer.set("class", "GeneralizedStudent");
    buffer.set("ν", ν);
    buffer.set("μ", μ);
    buffer.set("σ2", σ2);
  }
}

function DelayGeneralizedStudent(x:Random<Real>&, ν:Real, μ:Real, σ2:Real) -> DelayGeneralizedStudent {
  m:DelayGeneralizedStudent(x, ν, μ, σ2);
  return m;
}
