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

class ToyModel < HMMWithProposal<ToyModelParameter, ToyModelState, Random<Real>> {
  αx:Real <- 2.0;
  βx:Real <- 10.0;

  αy:Real <- 2.0;
  βy:Real <- 10.0;

  fiber parameter(θ:ToyModelParameter) -> Event {
    θ.σ2_x ~ InverseGamma(αx, βx);
    θ.σ2_y ~ InverseGamma(αy, βy);
  }

  fiber initial(x:ToyModelState, θ:ToyModelParameter) -> Event {
    x.x ~ Gaussian(0.0, 25.0);
    x.t <- 0;
  }

  fiber transition(x':ToyModelState, x:ToyModelState, θ:ToyModelParameter) -> Event {
    x'.t <- x.t + 1;
    auto μ <- x.x/2 + 25*x.x/(1.0 + x.x*x.x) + 8.0*cos(1.2*x'.t);
    x'.x ~ Gaussian(μ, θ.σ2_x);
  }

  fiber observation(y:Random<Real>, x:ToyModelState, θ:ToyModelParameter) -> Event {
    μ:Real <- x.x*x.x/20.0;
    y ~ Gaussian(μ, θ.σ2_y);
  }

  function propose(x:ForwardModel) -> (Real, Real) {

    auto x_old <- (HMMWithProposal<ToyModelParameter, ToyModelState, Random<Real>>?(x))!;

    auto θ_old <- x_old.θ; // Parameter from previous model
    
    auto σ2 <- 0.25;

    auto Q_x_old <- Normal(θ_old.σ2_x, σ2); // q(θ' | θ)
    θ.σ2_x <- Q_x_old.simulate(); // Draw new parameter for this model
    auto q_x <- Q_x_old.observe(θ.σ2_x);  // log q(θ | θ') (new given old)
    auto Q_x_new <- Normal(θ.σ2_x, σ2); // q(θ' | θ) 
    auto q_x_old <- Q_x_new.observe(θ_old.σ2_x); // log q(θ | θ') (old given new)


    auto Q_y_old <- Normal(θ_old.σ2_y, σ2); // q(θ' | θ)
    θ.σ2_y <- Q_y_old.simulate(); // Draw new parameter for this model
    auto q_y <- Q_y_old.observe(θ.σ2_y);  // log q(θ | θ') (new given old)
    auto Q_y_new <- Normal(θ.σ2_y, σ2); // q(θ' | θ) 
    auto q_y_old <- Q_y_new.observe(θ_old.σ2_y); // log q(θ | θ') (old given new)

    return (q_x+q_y, q_x_old+q_y_old);
  }
} 