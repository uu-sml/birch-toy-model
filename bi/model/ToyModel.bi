class ToyModelState {
  x:Random<Real>;
  t:Integer;

  function write(buffer:Buffer) {
    buffer.set("x", x);
    buffer.set("t", t);
  }
}

class ToyModelParameter {
  σ2_x:Random<Real>;
  σ2_y:Random<Real>;

  function write(buffer:Buffer) {
    buffer.set("sigma2_x", σ2_x);
    buffer.set("sigma2_y", σ2_y);
  }
}

class ToyModel < StateSpaceModel<ToyModelParameter, ToyModelState, Random<Real>> {
  αx:Real <- 2.01;
  βx:Real <- 10.01;

  αy:Real <- 2.01;
  βy:Real <- 10.01;

  fiber parameter(θ:ToyModelParameter) -> Event {
    θ.σ2_x ~ InverseGamma(αx, βx);
    θ.σ2_y ~ InverseGamma(αy, βy);
  }

  fiber initial(x:ToyModelState, θ:ToyModelParameter) -> Event {
    x.x ~ Gaussian(0.0, 25.0);
    x.t <- 0;
  }

  fiber transition(x':ToyModelState, x:ToyModelState, θ:ToyModelParameter) -> Event {
    auto μ <- x.x/2 + 25*x.x/(1.0 + x.x*x.x) + 8.0*cos(1.2*x.t);
    x'.x ~ Gaussian(μ, θ.σ2_x);
    x'.t <- x.t + 1;
  }

  fiber observation(y:Random<Real>, x:ToyModelState, θ:ToyModelParameter) -> Event {
    μ:Real <- x.x*x.x/20.0;
    y ~ Gaussian(μ, θ.σ2_y);
  }
}
