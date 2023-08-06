#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/arange.hpp>
#include <pythonic/include/numpy/multiply.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/ifloordiv.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/arange.hpp>
#include <pythonic/numpy/multiply.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/ifloordiv.hpp>
#include <pythonic/operator_/mul.hpp>
namespace __pythran_example_pythran
{
  struct cpu2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = long>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::lazy<__type0>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::multiply{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef decltype(std::declval<__type2>()(std::declval<__type1>(), std::declval<__type3>())) __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef __type0 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type1,__type5>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = long>
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& array1, argument_type1&& array2, argument_type2 nloops= 10L) const
    ;
  }  ;
  struct cpu1
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = long>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type2>())))>::type __type3;
      typedef typename __combined<__type1,__type3>::type __type4;
      typedef __type0 __ptype1;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type4>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = long>
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& array1, argument_type1&& array2, argument_type2 nloops= 10L) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename cpu2::type<argument_type0, argument_type1, argument_type2>::result_type cpu2::operator()(argument_type0&& array1, argument_type1&& array2, argument_type2 nloops) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef typename pythonic::lazy<__type0>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::multiply{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
    typedef decltype(std::declval<__type2>()(std::declval<__type1>(), std::declval<__type3>())) __type4;
    typedef typename pythonic::lazy<__type4>::type __type5;
    typedef typename __combined<__type1,__type5>::type __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::arange{})>::type>::type __type7;
    typedef long __type8;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type9;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type8>(), std::declval<__type9>()))) __type10;
    typedef typename pythonic::assignable<decltype(std::declval<__type7>()(std::declval<__type10>()))>::type __type11;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type12;
    typedef decltype(std::declval<__type12>()(std::declval<__type11>())) __type13;
    typedef decltype((pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type11>()))) __type14;
    typedef decltype((pythonic::operator_::add(std::declval<__type14>(), std::declval<__type13>()))) __type15;
    typedef decltype((pythonic::operator_::add(std::declval<__type15>(), std::declval<__type8>()))) __type16;
    typedef decltype((pythonic::operator_::add(std::declval<__type11>(), std::declval<__type16>()))) __type17;
    typedef typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type7>()(std::declval<__type10>()))>::type>::type __type18;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type19;
    typedef decltype(std::declval<__type19>()(std::declval<__type9>())) __type20;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type20>::type::iterator>::value_type>::type>::type i;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type20>::type::iterator>::value_type>::type>::type i_;
    typename pythonic::lazy<__type6>::type array1_ = array1;
    typename pythonic::assignable<typename __combined<__type11,__type17>::type>::type a = pythonic::numpy::functor::arange{}((pythonic::operator_::functor::floordiv{}(10000000L, nloops)));
    typename pythonic::assignable<typename __combined<__type18,__type16>::type>::type result = a;
    {
      for (long  i=0L; i < nloops; i += 1L)
      {
        result += (pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::mul(pythonic::numpy::functor::square{}(a), a)), pythonic::numpy::functor::square{}(a))), 2L));
      }
    }
    {
      for (long  i_=0L; i_ < nloops; i_ += 1L)
      {
        array1_ = pythonic::numpy::functor::multiply{}(array1_, array2);
      }
    }
    return array1_;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename cpu1::type<argument_type0, argument_type1, argument_type2>::result_type cpu1::operator()(argument_type0&& array1, argument_type1&& array2, argument_type2 nloops) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>())))>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::arange{})>::type>::type __type3;
    typedef long __type4;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type5;
    typedef decltype((pythonic::operator_::functor::floordiv{}(std::declval<__type4>(), std::declval<__type5>()))) __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type3>()(std::declval<__type6>()))>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type8;
    typedef decltype(std::declval<__type8>()(std::declval<__type7>())) __type9;
    typedef decltype((pythonic::operator_::mul(std::declval<__type9>(), std::declval<__type7>()))) __type10;
    typedef decltype((pythonic::operator_::add(std::declval<__type10>(), std::declval<__type9>()))) __type11;
    typedef decltype((pythonic::operator_::add(std::declval<__type11>(), std::declval<__type4>()))) __type12;
    typedef decltype((pythonic::operator_::add(std::declval<__type7>(), std::declval<__type12>()))) __type13;
    typedef typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type3>()(std::declval<__type6>()))>::type>::type __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type15;
    typedef decltype(std::declval<__type15>()(std::declval<__type5>())) __type16;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type>::type i;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type>::type i_;
    typename pythonic::assignable<typename __combined<__type0,__type2>::type>::type array1_ = array1;
    typename pythonic::assignable<typename __combined<__type7,__type13>::type>::type a = pythonic::numpy::functor::arange{}((pythonic::operator_::functor::floordiv{}(10000000L, nloops)));
    typename pythonic::assignable<typename __combined<__type14,__type12>::type>::type result = a;
    {
      for (long  i=0L; i < nloops; i += 1L)
      {
        result += (pythonic::operator_::add((pythonic::operator_::add((pythonic::operator_::mul(pythonic::numpy::functor::square{}(a), a)), pythonic::numpy::functor::square{}(a))), 2L));
      }
    }
    {
      for (long  i_=0L; i_ < nloops; i_ += 1L)
      {
        array1_ = (pythonic::operator_::mul(array1_, array2));
      }
    }
    return pythonic::types::make_tuple(array1_, array1_);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_example_pythran::cpu2::type<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, long>::result_type cpu20(pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array1, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu2()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu2::type<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, long>::result_type cpu21(pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array1, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu2()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, long>::result_type cpu22(pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array1, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu2()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, long>::result_type cpu23(pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array1, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu2()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu1::type<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, long>::result_type cpu10(pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array1, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu1()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu1::type<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, long>::result_type cpu11(pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array1, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu1()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu1::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>, long>::result_type cpu12(pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array1, pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu1()(array1, array2, nloops);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_example_pythran::cpu1::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>, long>::result_type cpu13(pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array1, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>&& array2, long&& nloops) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_example_pythran::cpu1()(array1, array2, nloops);
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
__pythran_wrap_cpu20(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu20(from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu21(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu21(from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu22(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu22(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu23(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu23(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu10(from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu11(from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_cpu13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"array1","array2","nloops", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(cpu13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_cpu2(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_cpu20(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu21(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu22(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu23(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "cpu2", "\n    - cpu2(uint8[:,:], uint8[:,:], int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_cpu1(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_cpu10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu11(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu12(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_cpu13(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "cpu1", "\n    - cpu1(uint8[:,:], uint8[:,:], int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "cpu2",
    (PyCFunction)__pythran_wrapall_cpu2,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n\n    - cpu2(uint8[:,:], uint8[:,:], int)"},{
    "cpu1",
    (PyCFunction)__pythran_wrapall_cpu1,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n\n    - cpu1(uint8[:,:], uint8[:,:], int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "example_pythran",            /* m_name */
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
PYTHRAN_MODULE_INIT(example_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(example_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("example_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.2",
                                      "2019-05-23 15:41:07.764162",
                                      "4858ca58ef514153e26b8fb4cc15f0d0aa4416bb045149a0c6493bb0adb0db78");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif