#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/include/__builtin__/assert.hpp>
#include <pythonic/include/__builtin__/enumerate.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/pythran/make_shape.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/log.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/idiv.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/assert.hpp>
#include <pythonic/__builtin__/enumerate.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/pythran/make_shape.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/log.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/idiv.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_tps_pythran
{
  struct compute_tps_matrix
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type>::type __type4;
      typedef long __type5;
      typedef decltype((pythonic::operator_::add(std::declval<__type4>(), std::declval<__type5>()))) __type6;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type7;
      typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type7>())) __type8;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type>::type __type9;
      typedef decltype((pythonic::operator_::add(std::declval<__type6>(), std::declval<__type9>()))) __type10;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type>::type __type11;
      typedef decltype(std::declval<__type1>()(std::declval<__type10>(), std::declval<__type11>())) __type12;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type12>()))>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type14;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>(), std::declval<__type11>())) __type15;
      typedef typename pythonic::assignable<decltype(std::declval<__type14>()(std::declval<__type15>()))>::type __type16;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type __type17;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type18;
      typedef decltype(std::declval<__type18>()(std::declval<__type9>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef decltype(std::declval<__type2>()[std::declval<__type20>()]) __type21;
      typedef decltype(std::declval<__type17>()(std::declval<__type21>())) __type22;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type22>::type::iterator>::value_type>::type __type23;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type23>::type>::type __type24;
      typedef typename pythonic::lazy<__type24>::type __type25;
      typedef decltype(std::declval<__type7>()[std::declval<__type20>()]) __type26;
      typedef decltype(std::declval<__type17>()(std::declval<__type26>())) __type27;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type27>::type::iterator>::value_type>::type __type28;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type28>::type>::type __type29;
      typedef typename pythonic::lazy<__type29>::type __type30;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type25>(), std::declval<__type30>())) __type31;
      typedef indexable<__type31> __type32;
      typedef typename __combined<__type16,__type32>::type __type33;
      typedef decltype(std::declval<__type18>()(std::declval<__type4>())) __type34;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type __type35;
      typedef decltype(std::declval<__type18>()(std::declval<__type11>())) __type36;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type36>::type::iterator>::value_type>::type __type37;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type35>(), std::declval<__type37>())) __type38;
      typedef indexable<__type38> __type39;
      typedef typename __combined<__type33,__type39>::type __type40;
      typedef typename __combined<__type40,__type32>::type __type41;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type42;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type28>::type>::type __type43;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type23>::type>::type>::type __type44;
      typedef decltype((std::declval<__type43>() - std::declval<__type44>())) __type45;
      typedef decltype(std::declval<__type42>()(std::declval<__type45>())) __type46;
      typedef container<typename std::remove_reference<__type46>::type> __type47;
      typedef typename __combined<__type41,__type47>::type __type48;
      typedef typename __combined<__type33,__type47>::type __type49;
      typedef typename pythonic::assignable<decltype(std::declval<__type49>()[std::declval<__type38>()])>::type __type50;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type51;
      typedef decltype(std::declval<__type51>()(std::declval<__type50>())) __type52;
      typedef decltype((pythonic::operator_::mul(std::declval<__type50>(), std::declval<__type52>()))) __type53;
      typedef decltype((pythonic::operator_::div(std::declval<__type53>(), std::declval<__type5>()))) __type54;
      typedef container<typename std::remove_reference<__type54>::type> __type55;
      typedef typename __combined<__type48,__type55>::type __type56;
      typedef typename __combined<__type56,__type39>::type __type57;
      typedef typename __combined<__type57,__type55>::type __type58;
      typedef container<typename std::remove_reference<__type58>::type> __type59;
      typedef typename __combined<__type13,__type59>::type __type60;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type61;
      typedef decltype(std::declval<__type61>()(std::declval<__type11>())) __type62;
      typedef container<typename std::remove_reference<__type62>::type> __type63;
      typedef typename __combined<__type60,__type63>::type __type64;
      typedef container<typename std::remove_reference<__type7>::type> __type65;
      typedef typename pythonic::returnable<typename __combined<__type64,__type65>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& new_pos, argument_type1&& centers) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 >
  typename compute_tps_matrix::type<argument_type0, argument_type1>::result_type compute_tps_matrix::operator()(argument_type0&& new_pos, argument_type1&& centers) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type5;
    typedef decltype(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type5>())) __type6;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type>::type __type7;
    typedef decltype(std::declval<__type1>()(std::declval<__type4>(), std::declval<__type7>())) __type8;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type8>()))>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type __type10;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type11;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type>::type __type12;
    typedef decltype(std::declval<__type11>()(std::declval<__type12>())) __type13;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
    typedef decltype(std::declval<__type2>()[std::declval<__type14>()]) __type15;
    typedef decltype(std::declval<__type10>()(std::declval<__type15>())) __type16;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type17>::type>::type __type18;
    typedef typename pythonic::lazy<__type18>::type __type19;
    typedef decltype(std::declval<__type5>()[std::declval<__type14>()]) __type20;
    typedef decltype(std::declval<__type10>()(std::declval<__type20>())) __type21;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type22>::type>::type __type23;
    typedef typename pythonic::lazy<__type23>::type __type24;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type24>())) __type25;
    typedef indexable<__type25> __type26;
    typedef typename __combined<__type9,__type26>::type __type27;
    typedef decltype(std::declval<__type11>()(std::declval<__type4>())) __type28;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type __type29;
    typedef decltype(std::declval<__type11>()(std::declval<__type7>())) __type30;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type30>::type::iterator>::value_type>::type __type31;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type29>(), std::declval<__type31>())) __type32;
    typedef indexable<__type32> __type33;
    typedef typename __combined<__type27,__type33>::type __type34;
    typedef typename __combined<__type34,__type26>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type36;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type22>::type>::type __type37;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type17>::type>::type>::type __type38;
    typedef decltype((std::declval<__type37>() - std::declval<__type38>())) __type39;
    typedef decltype(std::declval<__type36>()(std::declval<__type39>())) __type40;
    typedef container<typename std::remove_reference<__type40>::type> __type41;
    typedef typename __combined<__type35,__type41>::type __type42;
    typedef typename __combined<__type27,__type41>::type __type43;
    typedef typename pythonic::assignable<decltype(std::declval<__type43>()[std::declval<__type32>()])>::type __type44;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type45;
    typedef decltype(std::declval<__type45>()(std::declval<__type44>())) __type46;
    typedef decltype((pythonic::operator_::mul(std::declval<__type44>(), std::declval<__type46>()))) __type47;
    typedef long __type48;
    typedef decltype((pythonic::operator_::div(std::declval<__type47>(), std::declval<__type48>()))) __type49;
    typedef container<typename std::remove_reference<__type49>::type> __type50;
    typedef typename __combined<__type42,__type50>::type __type51;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type52;
    typedef decltype((pythonic::operator_::add(std::declval<__type4>(), std::declval<__type48>()))) __type53;
    typedef decltype((pythonic::operator_::add(std::declval<__type53>(), std::declval<__type12>()))) __type54;
    typedef decltype(std::declval<__type1>()(std::declval<__type54>(), std::declval<__type7>())) __type55;
    typedef typename pythonic::assignable<decltype(std::declval<__type52>()(std::declval<__type55>()))>::type __type56;
    typedef typename __combined<__type51,__type33>::type __type57;
    typedef typename __combined<__type57,__type50>::type __type58;
    typedef container<typename std::remove_reference<__type58>::type> __type59;
    typedef typename __combined<__type56,__type59>::type __type60;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type61;
    typedef decltype(std::declval<__type61>()(std::declval<__type7>())) __type62;
    typedef container<typename std::remove_reference<__type62>::type> __type63;
    typedef typename __combined<__type60,__type63>::type __type64;
    typedef container<typename std::remove_reference<__type5>::type> __type65;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type30>::type::iterator>::value_type>::type>::type inp_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type>::type ic_;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type>::type ind_d;
    typename pythonic::assignable<decltype(std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, new_pos)))>::type d = std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, new_pos));
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, new_pos)))>::type nb_new_pos = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, new_pos));
    ;
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, centers)))>::type nb_centers = std::get<1>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, centers));
    pythonic::pythran_assert((pythonic::operator_::eq(d, std::get<0>(pythonic::__builtin__::getattr(pythonic::types::attr::SHAPE{}, centers)))));
    typename pythonic::assignable<typename __combined<__type51,__type33>::type>::type EM = pythonic::numpy::functor::zeros{}(pythonic::__builtin__::pythran::functor::make_shape{}(nb_centers, nb_new_pos));
    {
      for (long  ind_d=0L; ind_d < d; ind_d += 1L)
      {
        {
          for (auto&& __tuple0: pythonic::__builtin__::functor::enumerate{}(centers.fast(ind_d)))
          {
            typename pythonic::assignable<decltype(std::get<1>(__tuple0))>::type center = std::get<1>(__tuple0);
            typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type ic = std::get<0>(__tuple0);
            {
              for (auto&& __tuple1: pythonic::__builtin__::functor::enumerate{}(new_pos.fast(ind_d)))
              {
                ;
                typename pythonic::lazy<decltype(std::get<0>(__tuple1))>::type inp = std::get<0>(__tuple1);
                EM[pythonic::types::make_tuple(ic, inp)] += pythonic::numpy::functor::square{}((std::get<1>(__tuple1) - center));
              }
            }
          }
        }
      }
    }
    {
      for (long  ic_=0L; ic_ < nb_centers; ic_ += 1L)
      {
        {
          for (long  inp_=0L; inp_ < nb_new_pos; inp_ += 1L)
          {
            typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type43>()[std::declval<__type32>()])>::type>::type tmp = EM.fast(pythonic::types::make_tuple(ic_, inp_));
            if ((pythonic::operator_::ne(tmp, 0L)))
            {
              EM.fast(pythonic::types::make_tuple(ic_, inp_)) = (pythonic::operator_::div((pythonic::operator_::mul(tmp, pythonic::numpy::functor::log{}(tmp))), 2L));
            }
          }
        }
      }
    }
    typename pythonic::assignable<typename __combined<__type64,__type65>::type>::type EM_ret = pythonic::numpy::functor::empty{}(pythonic::__builtin__::pythran::functor::make_shape{}((pythonic::operator_::add((pythonic::operator_::add(nb_centers, 1L)), d)), nb_new_pos));
    EM_ret(pythonic::types::contiguous_slice(pythonic::__builtin__::None,nb_centers),pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = EM;
    EM_ret(nb_centers,pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = pythonic::numpy::functor::ones{}(nb_new_pos);
    EM_ret(pythonic::types::contiguous_slice((pythonic::operator_::add(nb_centers, 1L)),(pythonic::operator_::add((pythonic::operator_::add(nb_centers, 1L)), d))),pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = new_pos;
    return EM_ret;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_tps_matrix0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& new_pos, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& centers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_tps_pythran::compute_tps_matrix()(new_pos, centers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type compute_tps_matrix1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& new_pos, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& centers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_tps_pythran::compute_tps_matrix()(new_pos, centers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_tps_matrix2(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& new_pos, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& centers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_tps_pythran::compute_tps_matrix()(new_pos, centers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type compute_tps_matrix3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& new_pos, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& centers) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_tps_pythran::compute_tps_matrix()(new_pos, centers);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_tps_matrix0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"new_pos","centers", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(compute_tps_matrix0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_tps_matrix1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"new_pos","centers", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(compute_tps_matrix1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_tps_matrix2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"new_pos","centers", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1]))
        return to_python(compute_tps_matrix2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_tps_matrix3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"new_pos","centers", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1]))
        return to_python(compute_tps_matrix3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_tps_matrix(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_tps_matrix0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_tps_matrix1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_tps_matrix2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_tps_matrix3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_tps_matrix", "\n    - compute_tps_matrix(float64[:,:], float64[:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_tps_matrix",
    (PyCFunction)__pythran_wrapall_compute_tps_matrix,
    METH_VARARGS | METH_KEYWORDS,
    "calculate the thin plate spline (tps) interpolation at a set of points\n\n    Supported prototypes:\n\n    - compute_tps_matrix(float64[:,:], float64[:,:])\n\n    Parameters\n    ----------\n\n    dsites: np.array\n        ``[nb_dim, M]`` array representing the postions of the M\n        'observation' sites, with nb_dim the space dimension.\n\n    centers: np.array\n        ``[nb_dim, N]`` array representing the postions of the N centers,\n        sources of the tps.\n\n    Returns\n    -------\n\n    EM : np.array\n        ``[(N+nb_dim), M]`` matrix representing the contributions at the M sites.\n\n        From unit sources located at each of the N centers, +\n        (nb_dim+1) columns representing the contribution of the linear\n        gradient part.\n\n    Notes\n    -----\n\n    >>> U_interp = np.dot(U_tps, EM)\n\n"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "tps_pythran",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(tps_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(tps_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("tps_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.2",
                                      "2019-05-23 15:41:03.954714",
                                      "ce43b7d670c80514e142b5f4e7206f2e076938ff0a4e3c7e8287ff9c893ae614");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif