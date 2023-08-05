#include <cstddef>
#include <iostream>
#include <vector>
#include "xbart.h"
#include <utility.h>
#include <forest.h>



using namespace std;

// Constructors
XBARTcpp::XBARTcpp(XBARTcppParams params){
	this->params = params;		
}
XBARTcpp::XBARTcpp (size_t M ,size_t N_sweeps ,
        size_t Nmin , size_t Ncutpoints , //CHANGE 
        double alpha , double beta , double tau , //CHANGE!
        size_t burnin, 
        size_t mtry , size_t max_depth_num, double kap , 
        double s , bool verbose , 
        bool draw_mu , bool parallel,int seed,size_t model_num,double no_split_penality){
  this->params.M = M; 
  this->params.N_sweeps = N_sweeps;
  this->params.Nmin = Nmin;
  this->params.Ncutpoints = Ncutpoints;
  this->params.alpha = alpha;
  this->params.beta = beta;
  this->params.tau = tau;
  this->params.burnin = burnin;
  this->params.mtry = mtry;
  this->params.max_depth_num = max_depth_num;
  this->params.kap = kap;
  this->params.s = s;
  this->params.verbose = verbose;
  this->params.draw_mu = draw_mu;
  this->params.parallel=parallel;
  this->trees =  vector< vector<tree>> (N_sweeps);
  this->model_num =  model_num;
  this->no_split_penality =  no_split_penality;

  // handling seed
  
  if(seed == -1){
    this->seed_flag = false;
    this->seed = 0;
  }else{
    this->seed_flag = true; 
    this->seed = (size_t)seed;
  }

  
  // Create trees3
  for(size_t i = 0; i < N_sweeps;i++){
        this->trees[i]=  vector<tree>(M); 
    }
  return;
}

XBARTcpp::XBARTcpp(std::string json_string){
  //std::vector<std::vector<tree>> temp_trees;
  from_json_to_forest(json_string,  this->trees,this->y_mean);  
  this->params.N_sweeps = this->trees.size();
  this->params.M = this->trees[0].size();
}

std::string XBARTcpp::_to_json(void){
  json j = get_forest_json(this->trees,this->y_mean);
  return j.dump(4);
}

// Getter
int XBARTcpp::get_M(){return((int)params.M);} 


void XBARTcpp::sort_x(int n,int d,double *a,int size, double *arr){
  xinfo x_std = XBARTcpp::np_to_xinfo(n,d,a);

  xinfo_sizet Xorder_std;
  ini_xinfo_sizet(Xorder_std, n, d);  
      for (size_t j = 0; j < d; j++)
    { 
        std::vector <double> x_temp (n);
        std::copy (x_std[j].begin(), x_std[j].end(), x_temp.begin());
        std::vector<size_t> temp = sort_indexes(x_temp);
        for (size_t i = 0; i < n; i++)
        {
            //cout << temp[i] << endl; 
            Xorder_std[j][i] = temp[i];
        }
    }
  std::copy(Xorder_std[d-1].begin(), Xorder_std[d-1].end(), arr);

}



void XBARTcpp::_predict(int n,int d,double *a){//,int size, double *arr){

  xinfo x_test_std = XBARTcpp::np_to_xinfo(n,d,a);
  vec_d x_test_std_2 = XBARTcpp::xinfo_to_col_major_vec(x_test_std); // INEFFICIENT

  ini_xinfo(this->yhats_test_xinfo, n, this->params.N_sweeps);

  double *Xtestpointer = &x_test_std_2[0];//&x_test_std[0][0];
  // predict_std(Xtestpointer,n,d,this->params.M,this->params.L,this->params.N_sweeps,
  //       this->yhats_test_xinfo,this->trees,this->y_mean); 
  predict_std(Xtestpointer,n,d,this->params.M,this->params.N_sweeps,
        this->yhats_test_xinfo,this->trees,this->y_mean); 
}


void XBARTcpp::_fit(int n,int d,double *a, 
      int n_y,double *a_y, size_t p_cat){
  
      xinfo x_std = XBARTcpp::np_to_xinfo(n,d,a);
      y_std.reserve(n_y);
      y_std = XBARTcpp::np_to_vec_d(n_y,a_y);
                
      // Calculate y_mean
      double y_mean = 0.0;
      for (size_t i = 0; i < n; i++){
          y_mean = y_mean + y_std[i];
        }
      y_mean = y_mean/(double)n;
      this->y_mean = y_mean;
      //   // xorder containers
      xinfo_sizet Xorder_std;
      ini_xinfo_sizet(Xorder_std, n, d);

      // MAKE MORE EFFICIENT! 
      // TODO: Figure out away of working on row major std::vectors
      // Fill in 
      for (size_t j = 0; j < d; j++)
    { 
        std::vector <double> x_temp (n);
        std::copy (x_std[j].begin(), x_std[j].end(), x_temp.begin());
        std::vector<size_t> temp = sort_indexes(x_temp);
        for (size_t i = 0; i < n; i++)
        {
            Xorder_std[j][i] = temp[i];
        }
    }
    // Create new x_std's that are row major
    vec_d x_std_2 = XBARTcpp::xinfo_to_col_major_vec(x_std); // INEFFICIENT - For now to include index sorting

    // Remove old x_std
    for(int j = 0; j<d;j++){
      x_std[j].clear();
      x_std[j].shrink_to_fit();
    }
    x_std.clear();
    x_std.shrink_to_fit();


      // // //max_depth_std container
      xinfo_sizet max_depth_std;

      ini_xinfo_sizet(max_depth_std, this->params.M, this->params.N_sweeps);
      // Fill with max Depth Value
      for(size_t i = 0; i < this->params.M; i++){
        for(size_t j = 0;j < this->params.N_sweeps; j++){
          max_depth_std[j][i] = this->params.max_depth_num;
        }
      }


      // Cpp native objects to return
      xinfo yhats_xinfo; // Temp Change
      ini_xinfo(yhats_xinfo, n, this->params.N_sweeps);


      // Temp Change
      ini_xinfo(this->sigma_draw_xinfo, this->params.M, this->params.N_sweeps);
      this->mtry_weight_current_tree.resize(d);
      //ini_xinfo(this->split_count_all_tree, d, this->params.M); // initialize at 0
      double *ypointer = &a_y[0];//&y_std[0];
      double *Xpointer = &x_std_2[0];//&x_std[0][0];


//size_t mtry, double kap, double s, bool verbose, bool draw_mu, bool parallel, xinfo &yhats_xinfo, xinfo &sigma_draw_xinfo, size_t p_categorical, size_t p_continuous, vector<vector<tree>> &trees, bool set_random_seed, size_t random_seed);
  if(this->model_num == 0){ // NORMAL
  fit_std(Xpointer,y_std,y_mean, Xorder_std,n,d,
                this->params.M,  this->params.N_sweeps, max_depth_std, 
                this->params.Nmin, this->params.Ncutpoints, this->params.alpha, 
                this->params.beta, this->params.tau, this->params.burnin, 
                this->params.mtry,  this->params.kap , 
                this->params.s, this->params.verbose,
                this->params.draw_mu, this->params.parallel,
                yhats_xinfo,this->sigma_draw_xinfo,this->mtry_weight_current_tree,p_cat,d-p_cat,this->trees,
                this->seed_flag, this->seed, this->no_split_penality);
  }else if(this->model_num == 1){
      fit_std_clt(Xpointer,y_std,y_mean, Xorder_std,n,d,
                this->params.M,  this->params.N_sweeps, max_depth_std, 
                this->params.Nmin, this->params.Ncutpoints, this->params.alpha, 
                this->params.beta, this->params.tau, this->params.burnin, 
                this->params.mtry,  this->params.kap , 
                this->params.s, this->params.verbose,
                this->params.draw_mu, this->params.parallel,
                yhats_xinfo,this->sigma_draw_xinfo,this->mtry_weight_current_tree,p_cat,d-p_cat,this->trees,
                this->seed_flag, this->seed, this->no_split_penality);
  }else if(this->model_num == 2){
          fit_std_probit(Xpointer,y_std,y_mean, Xorder_std,n,d,
                this->params.M,  this->params.N_sweeps, max_depth_std, 
                this->params.Nmin, this->params.Ncutpoints, this->params.alpha, 
                this->params.beta, this->params.tau, this->params.burnin, 
                this->params.mtry,  this->params.kap , 
                this->params.s, this->params.verbose,
                this->params.draw_mu, this->params.parallel,
                yhats_xinfo,this->sigma_draw_xinfo,this->mtry_weight_current_tree,p_cat,d-p_cat,this->trees,
                this->seed_flag, this->seed,this->no_split_penality);

  }
}    

// Getters
void XBARTcpp::get_yhats(int size,double *arr){
  xinfo_to_np(this->yhats_xinfo,arr);
}
void XBARTcpp::get_yhats_test(int size,double *arr){
  xinfo_to_np(this->yhats_test_xinfo,arr);
}
void XBARTcpp::get_sigma_draw(int size,double *arr){
  xinfo_to_np(this->sigma_draw_xinfo,arr);
}
void XBARTcpp::_get_importance(int size,double *arr){
  for(size_t i =0; i < size ; i++){
    arr[i] = this->mtry_weight_current_tree[i];
  }
}



// Private Helper Functions 

// Numpy 1D array to vec_d - std_vector of doubles
vec_d XBARTcpp::np_to_vec_d(int n,double *a){
  vec_d y_std(n,0);
  for (size_t i = 0; i < n; i++){
      y_std[i] = a[i];
     }
  return y_std;
}

vec_d XBARTcpp::np_to_col_major_vec(int n, int d,double *a){
  // 
  vec_d x_std(n*d,0);
  // Fill in Values of xinfo from array 
  ;
  for(size_t i =0;i<n;i++){
    for(size_t j =0;j<d;j++){
      size_t index = i*d + j;
      size_t index_std = j*n +i;
      x_std[index_std] = a[index];
    }
  }
  return x_std;
}

vec_d XBARTcpp::xinfo_to_col_major_vec(xinfo x_std){
  size_t n = (size_t)x_std[0].size();
  size_t d = (size_t)x_std.size();
  vec_d x_std_2(n*d,0);
  // Fill in Values of xinfo from array 
  for(size_t i =0;i<n;i++){
    for(size_t j =0;j<d;j++){
      size_t index_std = j*n +i;
      x_std_2[index_std] = x_std[j][i];
    }
  }
  return x_std_2;
}

// Numpy 2D Array to xinfo- nested std vectors of doubles
xinfo XBARTcpp::np_to_xinfo(int n, int d,double *a){
  // 
  xinfo x_std(d, vector<double> (n, 0));
  // Fill in Values of xinfo from array 
  for(size_t i =0;i<n;i++){
    for(size_t j =0;j<d;j++){
      size_t index = i*d + j;
      x_std[j][i] = a[index];
    }
  }
  return x_std;
}

void XBARTcpp::xinfo_to_np(xinfo x_std,double *arr){
  // Fill in array values from xinfo
  for(size_t i = 0 ,n = (size_t)x_std[0].size();i<n;i++){
    for(size_t j = 0,d = (size_t)x_std.size();j<d;j++){
      size_t index = i*d + j;
      arr[index] = x_std[j][i];
    }
  }
  return;
}

void XBARTcpp::test_random_generator(){
  std::default_random_engine generator;
  std::normal_distribution<double> normal_samp(0.0,0.0);

  cout << "Random Normal " << normal_samp(generator) <<endl;
}


