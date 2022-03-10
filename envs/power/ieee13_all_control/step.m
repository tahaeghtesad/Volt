function state = step(alpha, beta, gamma, c, repeat, t)
    global var
    % Algorithm parameters
    params.alpha = alpha;
    params.beta = beta;
    params.gamma = gamma;
    params.c = c;

    for i = 1:repeat
    	optdist_vc_ML(params, repeat * (t - 1) + i);
    end

    state.v = var.v_phase(:, repeat * t);
    state.q = var.q(:, repeat * t);
    state.fes = var.fes(repeat * t);
    state.f = var.f(repeat * t);

    state.v_c = var.v_c(:, repeat * t);
    state.lambda_bar = var.lambda_bar(:, repeat * t + 1);
    state.lambda_un = var.lambda_un(:, repeat * t + 1);
    state.xi = var.xi(:, repeat * t + 1);
    state.q_hat = var.q_hat(:, repeat * t);


end