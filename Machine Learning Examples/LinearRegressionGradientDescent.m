function [theta,cost] = LinearRegressionGradientDescent(X,Y,alpha,epsilon)
% function [theta,cost] = LinearRegressionGradientDescent(X,Y,alpha,epsilon)
% linea regression based on gradient descent
% input: X - feature matrix, each row represents one sample, first
%            column is always 1 
%        Y - output vector, each row represents one sample 
%        alpha - learning rate
%        epsilon - stopping criterion
% 
% output: theta - regression coeffients 
%         cost - min least square cost 
%


theta = pinv(X' * X)* (X'*Y);
error = Y' - theta'*X';
DJ = -error*X*2/max(size(theta));
theta = theta - alpha*DJ';


while(epsilon < norm(DJ) * alpha)
theta = pinv(X' * X)* (X'*Y);
error = Y' - theta'*X';
cost = -error*X*2/max(size(theta));
theta = theta - alpha*DJ';
end

error = Y' - theta'*X';
cost = error*error'/max(size(theta));













