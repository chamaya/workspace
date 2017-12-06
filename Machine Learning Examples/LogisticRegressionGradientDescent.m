function [theta,cost] = LogisticRegressionGradientDescent(X,Y,alpha,epsilon)
% function [theta,cost] = LogisticRegressionGradientDescent(X,Y,alpha,epsilon)
% logistic regression based on gradient descent
% input: X - feature matrix, each row represents one sample, first
%            column is always 1 
%        Y - output vector (binary: 1 or 0), each row represents one sample 
%        alpha - learning rate
%        epsilon - stopping criterion
% 
% output: theta - regression coeffients 
%         cost - logistic cost function 
%



% randomly initialize theta
theta = randn(size(X,2),1);
m = size(X,1); % the number of samples

n = 1;
grad = (X'*(1./(1+exp(-(X*theta-Y)))))./m;
while norm(grad) > epsilon
  grad = (X'*(1./(1+exp(-(X*theta-Y)))))./m;
  theta = theta - alpha * grad;
%  cost = 1/(2*m) * (  -Y .* log( 1./(1+exp(X*theta))) - (1-Y) .* log( 1 - 1./(1+exp(X*theta)))  );
%  if mod(n,100)==0,
%    fprintf(1,'n-iter: %d\tcost:%f\n',n,cost);
%  end 
  if norm(grad)<epsilon, break; end

  n = n + 1; 
end

cost = 1/(2*m) * (  -Y .* log( 1./(1+exp(-(X*theta)))) - (1-Y) .* log( 1 - 1./(1+exp(-(X*theta))))  );
%cost = sum(cost);
















