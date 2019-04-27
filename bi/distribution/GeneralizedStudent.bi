/**
 * Generalized Student's $t$-distribution.
 */
final class GeneralizedStudent(ν:Expression<Real>, μ:Expression<Real>, σ:Expression<Real> ) < Distribution<Real> {
  /**
   * Degrees of freedom.
   */
  ν:Expression<Real> <- ν;

  /**
   * Location parameter.
   */
  μ:Expression<Real> <- μ;

  /**
   * Scale parameter.
   */
  σ:Expression<Real> <- σ;

  function graft() {
    if delay? {
      delay!.prune();
    } else {
      delay <- DelayGeneralizedStudent(x, ν, μ, σ);
    }
  }

  function write(buffer:Buffer) {
    if delay? {
      delay!.write(buffer);
    } else {
      buffer.set("class", "GeneralizedStudent");
      buffer.set("ν", ν.value());
      buffer.set("μ", μ.value());
      buffer.set("σ", σ.value());
    }
  }
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Expression<Real>, μ:Expression<Real>, σ:Expression<Real> ) -> GeneralizedStudent {
  m:GeneralizedStudent(ν, μ, σ);
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Real, μ:Expression<Real>, σ:Expression<Real> ) -> GeneralizedStudent {
  m:GeneralizedStudent(Boxed(ν), μ, σ);
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Expression<Real>, μ:Real, σ:Expression<Real> ) -> GeneralizedStudent {
  m:GeneralizedStudent(ν, Boxed(μ), σ);
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Expression<Real>, μ:Expression<Real>, σ:Real ) -> GeneralizedStudent {
  m:GeneralizedStudent(ν, μ, Boxed(σ));
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Real, μ:Real, σ:Expression<Real> ) -> GeneralizedStudent { m:GeneralizedStudent(Boxed(ν), Boxed(μ), σ);
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Real, μ:Expression<Real>, σ:Real ) -> GeneralizedStudent {
  m:GeneralizedStudent(Boxed(ν), μ, Boxed(σ));
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Expression<Real>, μ:Real, σ:Real ) -> GeneralizedStudent {
  m:GeneralizedStudent(ν, Boxed(μ), Boxed(σ));
  return m;
}

/**
 * Create Generalized Student's $t$-distribution.
 */
function GeneralizedStudent(ν:Real, μ:Real, σ:Real ) -> GeneralizedStudent {
  m:GeneralizedStudent(Boxed(ν), Boxed(μ), Boxed(σ));
  return m;
}

