\\e=ellinit([0,0,1,-2248232106757,1329472091379662406]);
K=nfinit(a^2+3); e=ellinit([0,0,1,0,1],K)
\\K=nfinit(a^2-5); e=ellinit([1,a+1,a,a,0],K);

gendata(e,n,fileout)={
	my(v,i,j,p);
	v=vector(primepi(2^n));
	j=1;
	for(i=0,n-1,
		forprime(p=2^i,2^(i+1)-1,
			v[j]=ellap(e,p)/sqrt(p);j++
		);
		print(i+1);
	);
	write(fileout".txt",v);
}

gendata2(e,n,fileout)={
	my(v,i,j,p,pdec);
	v=vector(2*primepi(2^n));
	j=1;
	for(i=0,n-1,
		forprime(p=2^i,2^(i+1)-1,
			pdec=idealprimedec(K,p);
			if(length(pdec)==2,
				v[j]=ellap(e,pdec[1])/sqrt(p);j++;
				v[j]=ellap(e,pdec[2])/sqrt(p);j++
			,
				v[j]=1.*ellap(e,pdec[1])/p;j++
			);
		);
		print(i+1);
	);
	write(fileout".txt",vector(j-1,i,v[i]));
}


threem4()={
	my(nprimes,p,i,v);
	nprimes=0;
	v=vector(52);
	for(i=0,51,
		forprime(p=floor(2^(i/2))+1,2^((i+1)/2),if(p%4==3,nprimes++));
		v[i+1]=nprimes;
	);
	\\write("nprimes3m4.txt",v);
	return(v);
}

extra()={
	my(nprimes,p,v,w);
	v=vector(26);
	w=threem4();
	for(i=1,26,
		p=primepi(2^i);
		v[i]=2*p-w[2*i]-1;
	);
	write("newprimepi.txt",v);
}
