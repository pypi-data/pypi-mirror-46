#include "rtkTest.h"
#include "rtkMacro.h"
#include "rtkOraGeometryReader.h"
#include "rtkThreeDCircularProjectionGeometryXMLFile.h"
#include "rtkProjectionsReader.h"
#include "rtkMaskCollimationImageFilter.h"

#include <itkRegularExpressionSeriesFileNames.h>

/**
 * \file rtkoratest.cxx
 *
 * \brief Functional tests for classes managing Ora data (radART / medPhoton)
 *
 * This test reads and verifies the geometry from an ora projection.
 *
 * \author Simon Rit
 */

int main(int argc, char*argv[])
{
  if (argc < 3)
  {
    std::cerr << "Usage: " << std::endl;
    std::cerr << argv[0] << "oraGeometry.xml refGeometry.xml reference.mha" << std::endl;
    return EXIT_FAILURE;
  }

  std::cout << "Testing geometry..." << std::endl;

  // Ora geometry
  std::vector<std::string> filenames;
  filenames.emplace_back(argv[1]);
  rtk::OraGeometryReader::Pointer geoTargReader;
  geoTargReader = rtk::OraGeometryReader::New();
  geoTargReader->SetProjectionsFileNames( filenames );
  TRY_AND_EXIT_ON_ITK_EXCEPTION( geoTargReader->UpdateOutputData() );

  // Reference geometry
  rtk::ThreeDCircularProjectionGeometryXMLFileReader::Pointer geoRefReader;
  geoRefReader = rtk::ThreeDCircularProjectionGeometryXMLFileReader::New();
  geoRefReader->SetFilename(argv[2]);
  TRY_AND_EXIT_ON_ITK_EXCEPTION( geoRefReader->GenerateOutputInformation() )

  // Check geometries
  CheckGeometries(geoTargReader->GetGeometry(), geoRefReader->GetOutputObject() );

  // ******* COMPARING projections *******
  std::cout << "Testing attenuation conversion..." << std::endl;

  using OutputPixelType = float;
  constexpr unsigned int Dimension = 3;
  using ImageType = itk::Image< OutputPixelType, Dimension >;

  // Elekta projections reader
  using ReaderType = rtk::ProjectionsReader< ImageType >;
  ReaderType::Pointer reader = ReaderType::New();
  reader->SetFileNames( filenames );
  ReaderType::OutputImageSpacingType spacing;
  spacing[0] = 1.;
  spacing[1] = 2.;
  spacing[2] = 1.;
  reader->SetSpacing(spacing);
  ReaderType::OutputImagePointType origin(0.);
  reader->SetOrigin(0.);
  ReaderType::OutputImageDirectionType direction;
  direction.SetIdentity();
  reader->SetDirection(direction);

  // Create projection image filter
  using OFMType = rtk::MaskCollimationImageFilter<ImageType, ImageType>;
  OFMType::Pointer ofm = OFMType::New();
  ofm->SetInput( reader->GetOutput() );
  ofm->SetGeometry( geoTargReader->GetModifiableGeometry() );

  TRY_AND_EXIT_ON_ITK_EXCEPTION( ofm->Update() );

  // Reference projections reader
  ReaderType::Pointer readerRef = ReaderType::New();
  filenames.clear();
  filenames.emplace_back(argv[3]);
  readerRef->SetFileNames( filenames );
  TRY_AND_EXIT_ON_ITK_EXCEPTION(readerRef->Update());

  // 2. Compare read projections
  CheckImageQuality< ImageType >(ofm->GetOutput(), readerRef->GetOutput(), 1.e-10, 100000, 2000.0);

  // If all succeed
  std::cout << "\n\nTest PASSED! " << std::endl;
  return EXIT_SUCCESS;
}
