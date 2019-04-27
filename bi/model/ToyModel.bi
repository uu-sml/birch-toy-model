class ToyModelState {
  x:Random<Real>;
  t:Integer;
  
  function write(buffer:Buffer) {
    buffer.setReal("x", x);
    buffer.setReal("t", t);
  } 
}

class ToyModelParameter {
  σ2x:Real <- 10.0;
  σ2y:Real <- 10.0;
}

class ToyModel < StateSpaceModel<ToyModelParameter, ToyModelState, Random<Real>> {

  fiber initial(x:ToyModelState, θ:ToyModelParameter) -> Event {
    x.x ~ Gaussian(0.0, 25.0);
    x.t <- 0;
  }

  fiber transition(x':ToyModelState, x:ToyModelState, θ:ToyModelParameter) -> Event {
    auto μ <- x.x/2 + 25*x.x/(1.0 + x.x*x.x) + 8.0*cos(1.2*x.t);
    x'.x ~ Gaussian(μ, θ.σ2x);
    x'.t <- x.t + 1;
  }

  fiber observation(y:Random<Real>, x:ToyModelState, θ:ToyModelParameter) -> Event {
    μ:Real <- x.x*x.x/20.0;
    y ~ Gaussian(μ, θ.σ2y);
  }

}
