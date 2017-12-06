function [assign,clusters,cost] = kmeans(X,K)

c = randn(K,1);
clusters = repmat(c,size(X,2));
assign = zeros(size(X));
z = zeros(size(X,1),1);
for f = 1:size(X,2)
    cont = 1;
    %while(cont)
        feature = X(:,f);
        old_cluster = clusters(:,f);
        for j = 1:size(feature,1)
            z(j) = best_distance(feature(j),clusters(:,f));
        end
        for K_i = 1:K
            avgi = find(z == K_i);
            clusters(K_i,f) = mean(feature(avgi));
        end
        assign(:,f) = (z + f*K);
        cont = not(isequal(old_cluster, clusters(:,f)));
    %end
    
end

error = abs(X - clusters(assign));
cost = sum(error(:)) / size(X,1);
