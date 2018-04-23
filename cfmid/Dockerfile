
FROM ubuntu:16.04
MAINTAINER Tanvir Sajed

RUN echo "0.0.0" > /version

ENV BOOST_ROOT /opt/boost_1_55_0
ENV RDBASE=/opt/RDKit_2013_09_1
ENV CFM_ROOT=/opt/cfm
ENV LD_LIBRARY_PATH /opt/boost_1_55_0/lib:/opt/RDKit_2013_09_1/lib:/opt/lp_solve/lpsolve55/bin/ux64:/opt/liblbfgs/bin/lib:/usr/lib64:$LD_LIBRARY_PATH
ENV PATH /opt/cfm/bin:/opt/miniconda/bin:$PATH

RUN apt-get update && apt-get install -y -qq net-tools lsof wget tar xz-utils build-essential git mpich mpich-doc zip cmake libtool automake subversion openssh-server

EXPOSE 2200:22

# Installs boost libraries
RUN cd /opt;\
	wget http://sourceforge.net/projects/boost/files/boost/1.55.0/boost_1_55_0.tar.gz;\
	tar -xvzf boost_1_55_0.tar.gz;\
	cd /opt/boost_1_55_0;\
	./bootstrap.sh --prefix=. --with-libraries=regex,serialization,filesystem,system;\
	./b2 address-model=64 cflags=-fPIC cxxflags=-fPIC install

# Installs python for potential use of RDKit python wrappers
#RUN cd /opt;\
#	wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;\
#	chmod +x miniconda.sh;\
#	./miniconda.sh -p /opt/miniconda -b;\
#	conda update --yes conda;\
#	conda install --yes python=2.7
	
# Installs an LP Solver
RUN mkdir /usr/lib64;\
	cd /usr/lib64;\
	wget -O lp_solve.tar.gz https://sourceforge.net/projects/lpsolve/files/lpsolve/5.5.2.0/lp_solve_5.5.2.0_dev_ux64.tar.gz/download;\
	tar xvzf lp_solve.tar.gz

# Install liblbfgs
RUN cd /opt;\
	git clone https://github.com/chokkan/liblbfgs.git;\
	cd /opt/liblbfgs;\
	git checkout v1.10;\
	sh ./autogen.sh;\
	sh ./configure;\
	make;\
	make install

# download rdkit
RUN cd /opt;\
	wget -O rdkit.tar.gz https://sourceforge.net/projects/rdkit/files/rdkit/Q3_2013/RDKit_2013_09_1.tgz/download;\
	tar xvzf rdkit.tar.gz;\
	rm rdkit.tar.gz

# build and install rdkit
RUN cd /opt/RDKit_2013_09_1/External/INCHI-API;\
	wget -O INCHI-1-API.zip http://www.inchi-trust.org/download/104/INCHI-1-API.zip;\
	unzip INCHI-1-API.zip;\
	rm INCHI-1-API.zip;\
	mkdir src;\
	cp INCHI-1-API/INCHI_API/inchi_dll/* src/;\
	cd /opt/RDKit_2013_09_1;\
	mkdir build;\
	cd build;\		
	cmake .. -DRDK_BUILD_PYTHON_WRAPPERS=OFF -DRDK_BUILD_INCHI_SUPPORT=ON -DBOOST_ROOT=/opt/boost_1_55_0;\
	make install

#build and install cfm
RUN cd /opt;\
        svn checkout svn://svn.code.sf.net/p/cfm-id/code/cfm cfm;\
	cd cfm;\	
	mkdir build;\
	cd build;\
	cmake .. -DINCLUDE_TESTS=ON -DINCLUDE_TRAIN=ON -DLPSOLVE_INCLUDE_DIR=/usr/lib64 -DLPSOLVE_LIBRARY_DIR=/usr/lib64 \
	-DLBFGS_INCLUDE_DIR=/opt/liblbfgs/bin/include -DLBFGS_LIBRARY_DIR=/opt/liblbfgs/bin/lib;\
	make install

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
