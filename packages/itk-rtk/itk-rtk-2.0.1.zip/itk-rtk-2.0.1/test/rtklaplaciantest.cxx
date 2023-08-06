#include "itkRandomImageSource.h"
#include "rtkLaplacianImageFilter.h"
#include "rtkMacro.h"
#include "rtkTest.h"
#include "rtkDrawSheppLoganFilter.h"
#include "itkImageFileReader.h"
#include "rtkConstantImageSource.h"

#ifdef RTK_USE_CUDA
#include "rtkCudaLaplacianImageFilter.h"
#endif

/**
 * \file rtklaplaciantest.cxx
 *
 * \brief Tests whether the computation of the laplacian actually works
 *
 * This test generates a random volume and computes its laplacian.
 *
 * \author Cyril Mory
 */

int main(int argc, char*argv[])
{
  if (argc < 2)
  {
    std::cerr << "Usage: " << std::endl;
    std::cerr << argv[0] << " reference.mha" << std::endl;
    return EXIT_FAILURE;
  }

  using OutputPixelType = float;
  constexpr unsigned int Dimension = 3;

#ifdef USE_CUDA
  using OutputImageType = itk::CudaImage< OutputPixelType, Dimension >;
  using GradientImageType = itk::CudaImage<itk::CovariantVector<OutputPixelType, Dimension >, Dimension >;
#else
  using OutputImageType = itk::Image< OutputPixelType, Dimension >;
  using GradientImageType = itk::Image<itk::CovariantVector<OutputPixelType, Dimension >, Dimension >;
#endif

  // Constant image sources
  using ConstantImageSourceType = rtk::ConstantImageSource< OutputImageType >;
  ConstantImageSourceType::PointType origin;
  ConstantImageSourceType::SizeType size;
  ConstantImageSourceType::SpacingType spacing;

  ConstantImageSourceType::Pointer tomographySource  = ConstantImageSourceType::New();
  origin[0] = -127.;
  origin[1] = -127.;
  origin[2] = -127.;
#if FAST_TESTS_NO_CHECKS
  size[0] = 2;
  size[1] = 2;
  size[2] = 2;
  spacing[0] = 254.;
  spacing[1] = 254.;
  spacing[2] = 254.;
#else
  size[0] = 32;
  size[1] = 32;
  size[2] = 32;
  spacing[0] = 8.;
  spacing[1] = 8.;
  spacing[2] = 8.;
#endif
  tomographySource->SetOrigin( origin );
  tomographySource->SetSpacing( spacing );
  tomographySource->SetSize( size );
  tomographySource->SetConstant( 0. );

  // Generate a shepp logan phantom
  using DSLType = rtk::DrawSheppLoganFilter<OutputImageType, OutputImageType>;
  DSLType::Pointer dsl=DSLType::New();
  dsl->SetInput( tomographySource->GetOutput() );
  dsl->SetPhantomScale(128.);
  dsl->InPlaceOff();
  TRY_AND_EXIT_ON_ITK_EXCEPTION( dsl->Update() );


  // Read a reference image
  using ReaderType = itk::ImageFileReader<OutputImageType>;
  ReaderType::Pointer readerRef = ReaderType::New();
  readerRef->SetFileName(argv[1]);
  TRY_AND_EXIT_ON_ITK_EXCEPTION(readerRef->Update());


  std::cout << "\n\n****** Case 1: CPU laplacian ******" << std::endl;

  // Create and set the laplacian filter
  using LaplacianFilterType = rtk::LaplacianImageFilter<OutputImageType, GradientImageType>;
  LaplacianFilterType::Pointer laplacian = LaplacianFilterType::New();
  laplacian->SetInput(dsl->GetOutput());

  // Compute the laplacian of the shepp logan
  TRY_AND_EXIT_ON_ITK_EXCEPTION( laplacian->Update() );

  // Compare the result with the reference
  CheckImageQuality<OutputImageType>(laplacian->GetOutput(), readerRef->GetOutput(), 0.00001, 15, 2.0);

  std::cout << "\n\nTest PASSED! " << std::endl;

#ifdef USE_CUDA
  std::cout << "\n\n****** Case 2: CUDA laplacian ******" << std::endl;

  // Create and set the laplacian filter
  typedef rtk::CudaLaplacianImageFilter                		CUDALaplacianFilterType;
  CUDALaplacianFilterType::Pointer cudaLaplacian = CUDALaplacianFilterType::New();
  cudaLaplacian->SetInput(dsl->GetOutput());

  // Compute the laplacian of the shepp logan
  TRY_AND_EXIT_ON_ITK_EXCEPTION( cudaLaplacian->Update() );

  // Compare the result with the reference
  CheckImageQuality<OutputImageType>(cudaLaplacian->GetOutput(), readerRef->GetOutput(), 0.00001, 15, 2.0);

  std::cout << "\n\nTest PASSED! " << std::endl;
#endif

  return EXIT_SUCCESS;
}
