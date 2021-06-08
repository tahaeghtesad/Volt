function state = step(alpha, beta, gamma, c, t)
    tic
    global g_var

    % Algorithm parameters
    params.alpha = alpha;
    params.beta = beta;
    params.gamma = gamma;
    params.c = c;

    g_var = optdist_vc_ML(params, t);
    state = g_var
    toc
end