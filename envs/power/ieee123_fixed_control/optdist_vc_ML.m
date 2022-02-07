function optdist_vc_ML(params, t)

	global v_un v_bar q_un q_bar a b power_loss_ratio Y measurement_noise delay  n delay_flag control_flag U_c C  T noise_flag load_var
	global g_data var

	Data = g_data;

	alpha = params.alpha;
	beta = params.beta;
	gamma = params.gamma;
	c = params.c;

	proj0 = @(r) max(r,zeros(size(r)));


	% gradient handle
	X = inv(Y);
	nabla = @(qqq) a.*qqq + b ;
	nabla_indvidual = @(qqq,jjj) a(jjj)*qqq+b(jjj);
	f_func = @(qqq) sum(1/2*a.*(qqq.^2) + b.*qqq);

	if(t>1)
        if(delay_flag==0)
            GG = max(min(var.xi(:,t) + c.*(var.q_hat(:,t-1) - q_un),0), var.xi(:,t)+c.*(var.q_hat(:,t-1) - q_bar));
            comm_vector = nabla(var.q_hat(:,t-1)) + GG ;
            var.q_hat(:,t) = var.q_hat(:,t-1) - alpha.*(var.lambda_bar(:,t) - var.lambda_un(:,t) + power_loss_ratio*var.q_hat(:,t-1) + Y*(nabla(var.q_hat(:,t-1)) + GG ));
      %      q_hat(:,t) = q_hat(:,t-1) - alpha*(Y\(lambda_bar(:,t) - lambda_un(:,t) + power_loss_ratio*q_hat(:,t-1)) + (nabla(q_hat(:,t-1)) + GG ));
        else
            for iii=1:n
                comm_vector = zeros(n,1);
                i_neighbor = find(Y(iii,:)~=0); %neighboring buses of i
                for jjj=i_neighbor
                    if(jjj~=iii)
                        tau = randi(delay); % delayed value
                    else
                        tau=0;
                    end
                    delayed_t = max(t-tau,1);
                    delayed_t_minus = max(t-1-tau,1);
                    GG = max(min(var.xi(jjj,delayed_t) + c(jjj)*(var.q_hat(jjj,delayed_t_minus) - q_un(jjj)),0), var.xi(jjj,delayed_t)+c(jjj)*(var.q_hat(jjj,delayed_t_minus) - q_bar(jjj)));
                    comm_vector(jjj) = nabla_indvidual(var.q_hat(jjj,delayed_t_minus),jjj) + GG;
                end
                %GG = max(min(xi(:,t) + c*(q_hat(:,t-1) - q_un),0), xi(:,t)+c*(q_hat(:,t-1) - q_bar));
                %comm_vector = nabla(q_hat(:,t-1)) + GG );
                var.q_hat(iii,t) = var.q_hat(iii,t-1) - alpha(iii)*(var.lambda_bar(iii,t) - var.lambda_un(iii,t) + power_loss_ratio*var.q_hat(iii,t-1) + Y(iii,:)*comm_vector );
            end
        end


  end

  q(:,t) = max(min(var.q_hat(:,t),q_bar),q_un); % ''actuall implemented reactive power''

   % from previous equations, q(all)=G.Uc*qc
    q_inj=U_c*q(:,t);
% q_inj=zeros(12,t);

    if control_flag==1
        %[V_phase_pu] = OPENDSS_interface_qinj_static(t,load_var,q_inj,Data);
         [V_phase_pu] = pqinj_three_phase_static(Data,load_var,q_inj);
    end

    for h=1:length(V_phase_pu(:,1))
        v(h,t)=V_phase_pu(h,1)^2;
%         v_phase(h,t)=V_phase_pu(1,h);
    end

    for h=1:length(V_phase_pu(:,1))
        v_phase(h,t)=V_phase_pu(h,1);
    end
    %OpenDSS collects all phase voltages whereas we only need voltages for
    %control nodes
    % from prevous equations, vc=C*v(all)
    v_c(:,t)=C*v(:,t); % only squared control phase voltages
    v_c_phase(:,t)=C*v_phase(:,t); % actual control phase voltages
    f(t) = f_func(q(:,t));
    fes(t) =  norm( [proj0(v_c(:,t)-v_bar); proj0(v_un-v_c(:,t)); proj0(q(:,t)-q_bar); proj0(q_un-q(:,t))]);

 if(t<T)
        % update for the multipliers
        for i=1:n
            if var.q_hat(i,t) + var.xi(i,t)/c(i)<q_un(i)
                var.xi(i,t+1) = var.xi(i,t) + beta(i)*(var.q_hat(i,t) - q_un(i));
            elseif var.q_hat(i,t) + var.xi(i,t)/c(i) > q_bar(i)
                var.xi(i,t+1) = var.xi(i,t) + beta(i)*(var.q_hat(i,t) - q_bar(i));
            else
                var.xi(i,t+1) = (1 - beta(i)/c(i))*var.xi(i,t);
            end
        end
        %xi_bar(:,t+1) = max(xi_bar(:,t) + beta * (q_hat(:,t) - q_bar), 0);
        %xi_un(:,t+1)  = max(xi_un(:,t) + beta * (q_un - q_hat(:,t)),0);

        if(noise_flag==1)
            v_measurement = v_c(:,max(t-5,1));
            measurement_noise_at_t = randn(n,1)*measurement_noise;
            v_measurement = (sqrt(v_measurement)+measurement_noise_at_t).^2;
        else
            v_measurement = v_c(:,t);
        end

        var.lambda_bar(:,t+1) = max(var.lambda_bar(:,t) + gamma.* (v_measurement - v_bar),0);
        var.lambda_un(:,t+1) = max(var.lambda_un(:,t) + gamma.*(v_un - v_measurement),0);


        % Output class
%         var.v(:,t)=v(:,t);
%         var.v_phase(:,t)=v_phase(:,t);
        var.v_c(:,t)=v_c(:,t);
        var.v_c_phase(:,t)=v_c_phase(:,t);
        var.q(:,t)=q(:,t);
        var.fes(t)=fes(t);
        var.f(t)=f(t);

end