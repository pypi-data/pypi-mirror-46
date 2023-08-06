#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/__builtin__/zip.hpp>
#include <pythonic/include/numpy/log.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/where.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/idiv.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/zip.hpp>
#include <pythonic/numpy/log.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/where.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/idiv.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/types/slice.hpp>
namespace __pythran_subpix_pythran
{
  struct compute_subpix_2d_gaussian2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef long __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef pythonic::types::contiguous_slice __type3;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type3>(), std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::zip{})>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::where{})>::type>::type __type6;
      typedef decltype((pythonic::operator_::lt(std::declval<__type4>(), std::declval<__type0>()))) __type7;
      typedef decltype(std::declval<__type6>()(std::declval<__type7>())) __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type9>::type>::type __type11;
      typedef decltype(std::declval<__type5>()(std::declval<__type10>(), std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type13>::type>::type __type14;
      typedef typename pythonic::lazy<__type14>::type __type15;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type13>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type17>())) __type18;
      typedef indexable<__type18> __type19;
      typedef typename __combined<__type4,__type19>::type __type20;
      typedef double __type21;
      typedef container<typename std::remove_reference<__type21>::type> __type22;
      typedef typename __combined<__type20,__type22>::type __type23;
      typedef typename __combined<__type23,__type19>::type __type24;
      typedef typename __combined<__type24,__type22>::type __type25;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type0>(), std::declval<__type0>())) __type26;
      typedef decltype(std::declval<__type25>()[std::declval<__type26>()]) __type27;
      typedef decltype(std::declval<__type1>()(std::declval<__type27>())) __type28;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type28>()))) __type29;
      typedef decltype((pythonic::operator_::div(std::declval<__type29>(), std::declval<__type0>()))) __type30;
      typedef typename pythonic::assignable<long>::type __type31;
      typedef decltype((pythonic::operator_::add(std::declval<__type31>(), std::declval<__type29>()))) __type32;
      typedef typename __combined<__type31,__type32>::type __type33;
      typedef decltype((pythonic::operator_::add(std::declval<__type33>(), std::declval<__type29>()))) __type34;
      typedef typename __combined<__type33,__type34>::type __type35;
      typedef decltype((pythonic::operator_::add(std::declval<__type35>(), std::declval<__type29>()))) __type36;
      typedef typename __combined<__type35,__type36>::type __type37;
      typedef decltype((pythonic::operator_::add(std::declval<__type37>(), std::declval<__type29>()))) __type38;
      typedef typename __combined<__type37,__type38>::type __type39;
      typedef decltype((pythonic::operator_::add(std::declval<__type39>(), std::declval<__type29>()))) __type40;
      typedef typename __combined<__type39,__type40>::type __type41;
      typedef decltype((pythonic::operator_::add(std::declval<__type41>(), std::declval<__type29>()))) __type42;
      typedef typename __combined<__type41,__type42>::type __type43;
      typedef decltype((pythonic::operator_::add(std::declval<__type43>(), std::declval<__type29>()))) __type44;
      typedef typename __combined<__type43,__type44>::type __type45;
      typedef decltype((pythonic::operator_::add(std::declval<__type45>(), std::declval<__type29>()))) __type46;
      typedef typename __combined<__type45,__type46>::type __type47;
      typedef decltype((pythonic::operator_::add(std::declval<__type47>(), std::declval<__type29>()))) __type48;
      typedef typename __combined<__type47,__type48>::type __type49;
      typedef typename __combined<__type49,__type29>::type __type50;
      typedef decltype((pythonic::operator_::div(std::declval<__type50>(), std::declval<__type0>()))) __type51;
      typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type30>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>()))>::type __type52;
      typedef typename pythonic::assignable<typename std::tuple_element<3,typename std::remove_reference<__type52>::type>::type>::type __type53;
      typedef typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type52>::type>::type>::type __type54;
      typedef decltype((pythonic::operator_::mul(std::declval<__type53>(), std::declval<__type54>()))) __type55;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type52>::type>::type>::type __type56;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type56>()))) __type57;
      typedef typename pythonic::assignable<typename std::tuple_element<5,typename std::remove_reference<__type52>::type>::type>::type __type58;
      typedef decltype((pythonic::operator_::mul(std::declval<__type57>(), std::declval<__type58>()))) __type59;
      typedef decltype((std::declval<__type55>() - std::declval<__type59>())) __type60;
      typedef typename pythonic::assignable<typename std::tuple_element<4,typename std::remove_reference<__type52>::type>::type>::type __type61;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type61>()))) __type62;
      typedef decltype((pythonic::operator_::mul(std::declval<__type62>(), std::declval<__type58>()))) __type63;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type64;
      typedef decltype(std::declval<__type64>()(std::declval<__type53>())) __type65;
      typedef decltype((std::declval<__type63>() - std::declval<__type65>())) __type66;
      typedef decltype((pythonic::operator_::div(std::declval<__type60>(), std::declval<__type66>()))) __type67;
      typedef decltype((pythonic::operator_::mul(std::declval<__type53>(), std::declval<__type56>()))) __type68;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type54>()))) __type69;
      typedef decltype((pythonic::operator_::mul(std::declval<__type69>(), std::declval<__type61>()))) __type70;
      typedef decltype((std::declval<__type68>() - std::declval<__type70>())) __type71;
      typedef decltype((pythonic::operator_::div(std::declval<__type71>(), std::declval<__type66>()))) __type72;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type67>(), std::declval<__type72>(), std::declval<__type25>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& correl, argument_type1&& ix, argument_type2&& iy) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename compute_subpix_2d_gaussian2::type<argument_type0, argument_type1, argument_type2>::result_type compute_subpix_2d_gaussian2::operator()(argument_type0&& correl, argument_type1&& ix, argument_type2&& iy) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef pythonic::types::contiguous_slice __type1;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type1>()))>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::zip{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::where{})>::type>::type __type4;
    typedef long __type5;
    typedef decltype((pythonic::operator_::lt(std::declval<__type2>(), std::declval<__type5>()))) __type6;
    typedef decltype(std::declval<__type4>()(std::declval<__type6>())) __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type __type9;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type __type10;
    typedef decltype(std::declval<__type3>()(std::declval<__type9>(), std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type12>::type>::type __type13;
    typedef typename pythonic::lazy<__type13>::type __type14;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type12>::type>::type __type15;
    typedef typename pythonic::lazy<__type15>::type __type16;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type14>(), std::declval<__type16>())) __type17;
    typedef indexable<__type17> __type18;
    typedef typename __combined<__type2,__type18>::type __type19;
    typedef double __type20;
    typedef container<typename std::remove_reference<__type20>::type> __type21;
    typedef typename __combined<__type19,__type21>::type __type22;
    typedef typename pythonic::assignable<long>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type24;
    typedef typename __combined<__type22,__type18>::type __type25;
    typedef typename __combined<__type25,__type21>::type __type26;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type5>())) __type27;
    typedef decltype(std::declval<__type26>()[std::declval<__type27>()]) __type28;
    typedef decltype(std::declval<__type24>()(std::declval<__type28>())) __type29;
    typedef decltype((pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type29>()))) __type30;
    typedef decltype((pythonic::operator_::add(std::declval<__type23>(), std::declval<__type30>()))) __type31;
    typedef typename __combined<__type23,__type31>::type __type32;
    typedef decltype((pythonic::operator_::add(std::declval<__type32>(), std::declval<__type30>()))) __type33;
    typedef typename __combined<__type32,__type33>::type __type34;
    typedef decltype((pythonic::operator_::add(std::declval<__type34>(), std::declval<__type30>()))) __type35;
    typedef typename __combined<__type34,__type35>::type __type36;
    typedef decltype((pythonic::operator_::add(std::declval<__type36>(), std::declval<__type30>()))) __type37;
    typedef typename __combined<__type36,__type37>::type __type38;
    typedef decltype((pythonic::operator_::add(std::declval<__type38>(), std::declval<__type30>()))) __type39;
    typedef typename __combined<__type38,__type39>::type __type40;
    typedef decltype((pythonic::operator_::add(std::declval<__type40>(), std::declval<__type30>()))) __type41;
    typedef typename __combined<__type40,__type41>::type __type42;
    typedef decltype((pythonic::operator_::add(std::declval<__type42>(), std::declval<__type30>()))) __type43;
    typedef typename __combined<__type42,__type43>::type __type44;
    typedef decltype((pythonic::operator_::add(std::declval<__type44>(), std::declval<__type30>()))) __type45;
    typedef typename __combined<__type44,__type45>::type __type46;
    typedef decltype((pythonic::operator_::add(std::declval<__type46>(), std::declval<__type30>()))) __type47;
    typedef typename __combined<__type46,__type47>::type __type48;
    typedef decltype((pythonic::operator_::div(std::declval<__type30>(), std::declval<__type5>()))) __type49;
    typedef typename __combined<__type48,__type30>::type __type50;
    typedef decltype((pythonic::operator_::div(std::declval<__type50>(), std::declval<__type5>()))) __type51;
    typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type49>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>()))>::type __type52;
    typename pythonic::assignable<typename __combined<__type22,__type18>::type>::type correl_crop = correl(pythonic::types::contiguous_slice((iy - 1L),(pythonic::operator_::add(iy, 2L))),pythonic::types::contiguous_slice((ix - 1L),(pythonic::operator_::add(ix, 2L))));
    typename pythonic::lazy<decltype(pythonic::numpy::functor::where{}((pythonic::operator_::lt(correl_crop, 0L))))>::type tmp = pythonic::numpy::functor::where{}((pythonic::operator_::lt(correl_crop, 0L)));
    {
      for (auto&& __tuple0: pythonic::__builtin__::functor::zip{}(std::get<0>(tmp), std::get<1>(tmp)))
      {
        typename pythonic::lazy<decltype(std::get<1>(__tuple0))>::type i1 = std::get<1>(__tuple0);
        typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type i0 = std::get<0>(__tuple0);
        correl_crop[pythonic::types::make_tuple(i0, i1)] = 1e-06;
      }
    }
    typename pythonic::assignable<typename __combined<__type48,__type30>::type>::type c10 = 0L;
    typename pythonic::assignable<typename __combined<__type48,__type30>::type>::type c01 = 0L;
    typename pythonic::assignable<typename __combined<__type48,__type30>::type>::type c11 = 0L;
    typename pythonic::assignable<typename __combined<__type48,__type30>::type>::type c20 = 0L;
    typename pythonic::assignable<typename __combined<__type48,__type30>::type>::type c02 = 0L;
    ;
    ;
    c10 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L)))));
    c01 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L)))));
    c11 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L)))));
    c01 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L)))));
    c11 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L)))));
    c02 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L)))));
    c01 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L)))));
    c11 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L)))));
    ;
    ;
    ;
    c10 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L)))));
    c01 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L)))));
    c11 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L)))));
    c20 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L)))));
    c01 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L)))));
    c11 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L)))));
    c20 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L)))));
    c02 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L)))));
    c01 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L)))));
    c11 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L)))));
    c20 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L)))));
    ;
    ;
    ;
    c10 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L)))));
    c01 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L)))));
    c11 += (pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L)))));
    c01 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L)))));
    c11 += (pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L)))));
    c02 += (pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L)))));
    ;
    ;
    c10 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))));
    c01 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))));
    c11 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))));
    c20 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))));
    c02 += (pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))));
    ;
    typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type49>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>(), std::declval<__type51>()))>::type>::type __tuple1 = pythonic::types::make_tuple((pythonic::operator_::div((pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))))), 9L)), (pythonic::operator_::div(c10, 6L)), (pythonic::operator_::div(c01, 6L)), (pythonic::operator_::div(c11, 4L)), (pythonic::operator_::div(c20, 6L)), (pythonic::operator_::div(c02, 6L)));
    ;
    typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type52>::type>::type>::type>::type c10_ = std::get<1>(__tuple1);
    typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type52>::type>::type>::type>::type c01_ = std::get<2>(__tuple1);
    typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<3,typename std::remove_reference<__type52>::type>::type>::type>::type c11_ = std::get<3>(__tuple1);
    typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<4,typename std::remove_reference<__type52>::type>::type>::type>::type c20_ = std::get<4>(__tuple1);
    typename pythonic::assignable<typename pythonic::assignable<typename std::tuple_element<5,typename std::remove_reference<__type52>::type>::type>::type>::type c02_ = std::get<5>(__tuple1);
    ;
    ;
    return pythonic::types::make_tuple((pythonic::operator_::div(((pythonic::operator_::mul(c11_, c01_)) - (pythonic::operator_::mul((pythonic::operator_::mul(2L, c10_)), c02_))), ((pythonic::operator_::mul((pythonic::operator_::mul(4L, c20_)), c02_)) - pythonic::numpy::functor::square{}(c11_)))), (pythonic::operator_::div(((pythonic::operator_::mul(c11_, c10_)) - (pythonic::operator_::mul((pythonic::operator_::mul(2L, c01_)), c20_))), ((pythonic::operator_::mul((pythonic::operator_::mul(4L, c20_)), c02_)) - pythonic::numpy::functor::square{}(c11_)))), correl_crop);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_subpix_pythran::compute_subpix_2d_gaussian2::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long, long>::result_type compute_subpix_2d_gaussian20(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& correl, long&& ix, long&& iy) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_subpix_pythran::compute_subpix_2d_gaussian2()(correl, ix, iy);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_subpix_pythran::compute_subpix_2d_gaussian2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long, long>::result_type compute_subpix_2d_gaussian21(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& correl, long&& ix, long&& iy) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_subpix_pythran::compute_subpix_2d_gaussian2()(correl, ix, iy);
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
__pythran_wrap_compute_subpix_2d_gaussian20(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"correl","ix","iy", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(compute_subpix_2d_gaussian20(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_subpix_2d_gaussian21(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"correl","ix","iy", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(compute_subpix_2d_gaussian21(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_subpix_2d_gaussian2(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_subpix_2d_gaussian20(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_subpix_2d_gaussian21(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_subpix_2d_gaussian2", "\n    - compute_subpix_2d_gaussian2(float32[:,:], int, int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_subpix_2d_gaussian2",
    (PyCFunction)__pythran_wrapall_compute_subpix_2d_gaussian2,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n\n    - compute_subpix_2d_gaussian2(float32[:,:], int, int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "subpix_pythran",            /* m_name */
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
PYTHRAN_MODULE_INIT(subpix_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(subpix_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("subpix_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.2",
                                      "2019-05-23 15:41:07.512411",
                                      "e37f4fc56404ede99cfd588577b1d87dc7ab254032902412881b08bd0861e7fb");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif