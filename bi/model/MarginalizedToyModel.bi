class MarginalizedToyModelState {
  x:Random<Real>;
  t:Integer;
  χx:Real;
  νx:Real;
  χy:Real;
  νy:Real;
  
  function write(buffer:Buffer) {
    buffer.set("x", x);
    buffer.set("t", t);
    buffer.set("χx",χx);
    buffer.set("νx",νx);
    buffer.set("χy",χy);
    buffer.set("νy",νy);
  } 
}

class MarginalizedToyModelParameter {}

class MarginalizedToyModel < StateSpaceModel<MarginalizedToyModelParameter, MarginalizedToyModelState, Random<Real>> {

  fiber initial(x:MarginalizedToyModelState, θ:MarginalizedToyModelParameter) -> Event {
    x.x ~ Gaussian(0.0, 25.0);
    x.t <- 0;
    x.χx <- -10.0;
    x.νx <- 2.0;
    x.χy <- -1.0;
    x.νy <- 2.0;
  }

  fiber transition(x':MarginalizedToyModelState, x:MarginalizedToyModelState, θ:MarginalizedToyModelParameter) -> Event {
    // Compute propagation parameters
    auto ν <- x.νx + 2; // Degrees of freedom
    auto μ <- x.x/2 + 25*x.x/(1.0 + x.x*x.x) + 8.0*cos(1.2*x.t); // Mean
    auto σ <- -2*x.χx / ν; // Scale

    // Propagate
    x'.x ~ GeneralizedStudent(ν, μ, σ);

    // Update statistics for the next state
    x'.χx <- x.χx -pow(x'.x - μ, 2)/2;
    x'.νx <- x.νx + 1;
    x'.χy <- x.χy;
    x'.νy <- x.νy;
    x'.t <- x.t + 1;
  }

  fiber observation(y:Random<Real>, x:MarginalizedToyModelState, θ:MarginalizedToyModelParameter) -> Event {
    // Compute observation parameters
    auto ν <- x.νy + 2; // Degrees of freedom
    μ:Real <- x.x*x.x/20.0; // Mean
    auto σ2 <- -2*x.χy / ν; // Scale
    //stdout.print(x.t);
    //stdout.print("\n");
    //stdout.print(σ2);

    // Observe
    y ~ GeneralizedStudent(ν, μ, σ2);

    // Update statistics
    x.χy <- x.χy - pow(y - μ, 2)/2;
    x.νy <- x.νy + 1;
  }

}
