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
    %state = data;

%    disp(alpha)
%    disp(beta)
%    disp(gamma)
%    disp(c)
%    disp(state)
end