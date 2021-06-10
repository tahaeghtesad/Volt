function state = step(alpha, beta, gamma, c, t)
    global g_var
    % Algorithm parameters
    params.alpha = alpha;
    params.beta = beta;
    params.gamma = gamma;
    params.c = c;

    data = optdist_vc_ML(params, t);

    state.v = data.v(:, t);
    state.q = data.q(:, t);
    state.fes = data.fes(t);

    g_var = data

%    disp(alpha)
%    disp(beta)
%    disp(gamma)
%    disp(c)
%    disp(state)
end